from hashlib import sha256
import secrets
from uuid import uuid4

import jwt
from pwdlib import PasswordHash

from app.authentication.authentication_model import (
    AccessTokenPayloadModel,
    LoginRequestModel,
    RefreshTokenRequestModel,
    ResetPasswordBodyModel,
    TokenResponseModel,
    UserSessionCreateModel,
)
from app.authentication.authentication_repository import (
    AuthenticationRepository,
)
from app.authentication.services.session_service import session_service
from app.users.users_service import users_service
from app.users.users_model import UsersRequestModel
from config.db_dependencies import get_connection_handler
from app.exceptions.exceptions import (
    AccessTokenExpiredException,
    InactiveUserException,
    InvalidAccessTokenException,
    InvalidCredentialsException,
    RefreshTokenExpiredException,
    SessionRevokedException,
    SessionNotFoundException,
    ResetPasswordException,
    UserNotFoundException
)
from config.settings import get_settings
from datetime import datetime, timedelta, timezone

class AuthenticationService():
    def __init__(self) -> None:
        self._authentication_repository = AuthenticationRepository(
            connection_handler_factory=get_connection_handler,
        )
        self._session_service = session_service
        self._users_service = users_service
        self._password_hash = PasswordHash.recommended()
        self._settings = get_settings()

    def login(
        self,
        login_data: LoginRequestModel,
    ) -> TokenResponseModel:
        email = login_data.email.strip().lower()

        user = (
            self._authentication_repository
            .select_user_credentials_by_email(email=email)
        )

        if user is None:
            raise InvalidCredentialsException()

        password_is_valid = self._password_hash.verify(
            login_data.password,
            user.password_hash,
        )

        if not password_is_valid:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise InactiveUserException()

        now = datetime.now(timezone.utc)

        refresh_token = self._create_refresh_token()
        refresh_token_hash = self._hash_refresh_token(
            refresh_token=refresh_token,
        )

        refresh_expires_at = now + timedelta(
            days=self._settings.refresh_token_expire_days,
        )

        session = self._session_service.create_session(
            session=UserSessionCreateModel(
                user_id=user.id,
                refresh_token_hash=refresh_token_hash,
                expires_at=refresh_expires_at,
            )
        )

        access_token = self._create_access_token(
            user_id=user.id,
            session_id=session.id,
            now=now,
        )

        return self._build_token_response(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def reset_password(
        self,
        reset_password_data: ResetPasswordBodyModel,
    ) -> None:
        now = datetime.now(timezone.utc)

        refresh_token_hash = self._hash_refresh_token(
            refresh_token=reset_password_data.refresh_token,
        )

        session = (
            self._session_service
            .get_session_by_refresh_token_hash(
                refresh_token_hash=refresh_token_hash,
            )
        )

        session_expires_at = self._as_utc(
            value=session.expires_at,
        )

        if session.revoked_at is not None:
            raise SessionRevokedException()
    
        if now >= session_expires_at:
            raise RefreshTokenExpiredException()
        
        self._users_service.reset_password(
            user_id=session.user_id,
            new_password=reset_password_data.new_password,
        )

        self._session_service.revoke_all_user_sessions(
            user_id=session.user_id,
        )

    def refresh(
        self,
        refresh_data: RefreshTokenRequestModel,
    ) -> TokenResponseModel:
        now = datetime.now(timezone.utc)

        current_refresh_token_hash = self._hash_refresh_token(
            refresh_token=refresh_data.refresh_token,
        )

        session = (
            self._session_service
            .get_session_by_refresh_token_hash(
                refresh_token_hash=current_refresh_token_hash,
            )
        )

        if session.revoked_at is not None:
            raise SessionRevokedException()

        session_expires_at = self._as_utc(
            value=session.expires_at,
        )

        if now >= session_expires_at:
            raise RefreshTokenExpiredException()

        new_refresh_token = self._create_refresh_token()

        new_refresh_token_hash = self._hash_refresh_token(
            refresh_token=new_refresh_token,
        )

        new_expires_at = now + timedelta(
            days=self._settings.refresh_token_expire_days,
        )

        rotated_session = self._session_service.rotate_refresh_token(
            session_id=session.id,
            current_refresh_token_hash=current_refresh_token_hash,
            new_refresh_token_hash=new_refresh_token_hash,
            new_expires_at=new_expires_at,
            last_used_at=now,
        )

        access_token = self._create_access_token(
            user_id=rotated_session.user_id,
            session_id=rotated_session.id,
            now=now,
        )

        return self._build_token_response(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )

    def logout(
        self,
        refresh_data: RefreshTokenRequestModel,
    ) -> None:
        refresh_token_hash = self._hash_refresh_token(
            refresh_token=refresh_data.refresh_token,
        )

        session = (
            self._session_service
            .get_session_by_refresh_token_hash(
                refresh_token_hash=refresh_token_hash,
            )
        )

        if session.revoked_at is not None:
            return

        self._session_service.revoke_session(
            user_id=session.user_id,
            session_id=session.id,
        )
        
    def validate_access_token(
        self,
        access_token: str,
    ) -> AccessTokenPayloadModel:
        try:
            payload = jwt.decode(
                access_token,
                self._settings.jwt_secret_key,
                algorithms=[self._settings.jwt_algorithm],
                issuer=self._settings.jwt_issuer,
                audience=self._settings.jwt_audience,
                options={
                    "require": [
                        "sub",
                        "sid",
                        "type",
                        "jti",
                        "iat",
                        "exp",
                        "iss",
                        "aud",
                    ],
                },
            )

        except jwt.ExpiredSignatureError as error:
            raise AccessTokenExpiredException() from error

        except jwt.InvalidTokenError as error:
            raise InvalidAccessTokenException() from error

        if payload.get("type") != "access":
            raise InvalidAccessTokenException()

        try:
            token_payload = AccessTokenPayloadModel.model_validate(
                payload
            )
        except ValueError as error:
            raise InvalidAccessTokenException() from error

        try:
            session = self._session_service.get_session_by_id(
                session_id=token_payload.sid,
            )
        except SessionNotFoundException as error:
            raise InvalidAccessTokenException() from error

        if session.user_id != token_payload.sub:
            raise InvalidAccessTokenException()

        if session.revoked_at is not None:
            raise SessionRevokedException()

        return token_payload

    def _create_access_token(
        self,
        user_id: str,
        session_id: str,
        now: datetime,
    ) -> str:
        expires_at = now + timedelta(
            minutes=self._settings.access_token_expire_minutes,
        )

        payload = {
            "sub": user_id,
            "sid": session_id,
            "type": "access",
            "jti": str(uuid4()),
            "iat": now,
            "exp": expires_at,
            "iss": self._settings.jwt_issuer,
            "aud": self._settings.jwt_audience,
        }

        return jwt.encode(
            payload,
            self._settings.jwt_secret_key,
            algorithm=self._settings.jwt_algorithm,
        )

    def _create_refresh_token(self) -> str:
        return secrets.token_urlsafe(64)

    def _hash_refresh_token(
        self,
        refresh_token: str,
    ) -> str:
        return sha256(
            refresh_token.encode("utf-8")
        ).hexdigest()

    def _build_token_response(
        self,
        access_token: str,
        refresh_token: str,
    ) -> TokenResponseModel:
        return TokenResponseModel(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_in=(
                self._settings.access_token_expire_minutes * 60
            ),
        )

    def _as_utc(
        self,
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)
    
authentication_service = AuthenticationService()
