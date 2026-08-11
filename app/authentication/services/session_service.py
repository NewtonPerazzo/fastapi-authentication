from datetime import datetime

from app.authentication.authentication_repository import AuthenticationRepository
from app.authentication.authentication_model import (
    UserSessionModel,
    UserSessionCreateModel
)
from config.db_dependencies import get_connection_handler
from app.exceptions.exceptions import (
    InvalidRefreshTokenException,
    SessionNotFoundException,
)

class SessionService():
    def __init__(self) -> None:
        self._repository = AuthenticationRepository(
            connection_handler_factory=get_connection_handler,
        )

    def create_session(
        self,
        session: UserSessionCreateModel
    ) -> UserSessionModel:
        return self._repository.create(
            session=session
        )

    def revoke_session(
        self,
        user_id: str,
        session_id: str
    ) -> UserSessionModel:
        revoked_session = self._repository.revoke_session(
            user_id=user_id,
            session_id=session_id
        )

        if not revoked_session:
            raise SessionNotFoundException()

        return revoked_session

    def revoke_all_user_sessions(
        self,
        user_id: str,
    ) -> bool:
        return self._repository.revoke_all_user_sessions(
            user_id=user_id
        )
        
    def delete_expired_sessions(
        self
    ) -> int:
        return self._repository.delete_expired_sessions()

    def delete_expired_sessions_by_user(
        self,
        user_id: str
    ) -> int:
        return self._repository.delete_expired_sessions_by_user(
            user_id=user_id,
        )

    def get_session_by_id(
        self,
        session_id: str,
    ) -> UserSessionModel:
        session = self._repository.select_session_by_id(
            session_id=session_id,
        )

        if session is None:
            raise SessionNotFoundException()

        return session
    def get_session_by_user_id(
        self,
        user_id: str,
    ) -> UserSessionModel:
        session = self._repository.select_session_by_user_id(
            user_id=user_id
        )

        if session is None:
            raise SessionNotFoundException()

        return session

    def get_session_by_refresh_token_hash(
        self,
        refresh_token_hash: str,
    ) -> UserSessionModel:
        session = self._repository.select_session_by_refresh_token_hash(
            refresh_token_hash=refresh_token_hash,
        )

        if session is None:
            raise InvalidRefreshTokenException()

        return session

    def rotate_refresh_token(
        self,
        session_id: str,
        current_refresh_token_hash: str,
        new_refresh_token_hash: str,
        new_expires_at: datetime,
        last_used_at: datetime,
    ) -> UserSessionModel:
        session = self._repository.update_session_refresh_token(
            session_id=session_id,
            refresh_token_hash=current_refresh_token_hash,
            new_refresh_token_hash=new_refresh_token_hash,
            new_expires_at=new_expires_at,
            new_last_used_at=last_used_at,
        )

        if session is None:
            raise InvalidRefreshTokenException()

        return session

session_service = SessionService()
