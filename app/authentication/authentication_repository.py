from collections.abc import Callable
from app.users.users_entity import UsersEntity
from app.authentication.authentication_entity import UsersSessionEntity
from config.db_connection import DBConnectionHandler
from sqlalchemy.exc import SQLAlchemyError
from app.authentication.authentication_model import (
    UserCredentialsModel, 
    UserSessionCreateModel,
    UserSessionModel
)
from datetime import datetime, timezone

class AuthenticationRepository():
    def __init__(
        self,
        connection_handler_factory: Callable[[], DBConnectionHandler],
    ) -> None:
        self.__connection_handler_factory = connection_handler_factory

    def select_user_credentials_by_email(
        self,
        email: str
    ) -> UserCredentialsModel | None:
        with self.__connection_handler_factory() as db:
            try:
                user = db.session.query(UsersEntity) \
                    .filter(UsersEntity.email == email) \
                    .first()

                if user:
                    user_normalized = {
                        "id": user.id,
                        "email": user.email,
                        "password_hash": user.password_hash,
                        "is_active": user.is_active,
                        "password_changed_at": user.password_changed_at
                    }
                    return UserCredentialsModel.model_validate(user_normalized)
                return None
            except SQLAlchemyError:
                db.session.rollback()
                raise
            
    def create(
        self,
        session: UserSessionCreateModel
    ) -> UserSessionModel:
        with self.__connection_handler_factory() as db:
            try:
                user_session_entity = UsersSessionEntity(**session.model_dump())
                db.session.add(user_session_entity)
                db.session.commit()
                db.session.refresh(user_session_entity)
                return UserSessionModel.model_validate(user_session_entity)
            except SQLAlchemyError:
                db.session.rollback()
                raise

    def select_session_by_refresh_token_hash(
        self,
        refresh_token_hash: str
    ) -> UserSessionModel | None:
        with self.__connection_handler_factory() as db:
            try:
                session = db.session.query(UsersSessionEntity) \
                    .filter(UsersSessionEntity.refresh_token_hash == refresh_token_hash) \
                    .first()
            
                return UserSessionModel.model_validate(session) if session else None
            except SQLAlchemyError:
                db.session.rollback()
                raise

    def update_session_refresh_token(
        self,
        session_id: str,
        refresh_token_hash: str,
        new_refresh_token_hash: str,
        new_expires_at: datetime,
        new_last_used_at: datetime
    ) -> UserSessionModel | None:
        with self.__connection_handler_factory() as db:
            try:
                session_entity = db.session.query(UsersSessionEntity) \
                    .filter(UsersSessionEntity.refresh_token_hash == refresh_token_hash)\
                    .where(UsersSessionEntity.id == session_id) \
                    .first()

                if session_entity is None:
                    return None

                session_entity.refresh_token_hash = new_refresh_token_hash
                session_entity.expires_at = new_expires_at
                session_entity.last_used_at = new_last_used_at  

                db.session.commit()
                db.session.refresh(session_entity)
                return UserSessionModel.model_validate(session_entity)

            except SQLAlchemyError:
                db.session.rollback()
                raise
        
    def revoke_session(
        self,
        user_id: str,
        session_id: str
    ) -> UserSessionModel | None:
        with self.__connection_handler_factory() as db:
            try:
                session_entity = db.session.query(UsersSessionEntity) \
                    .filter(UsersSessionEntity.user_id == user_id) \
                    .where(UsersSessionEntity.id == session_id) \
                    .first()

                if session_entity is None:
                    return None
                
                session_entity.revoked_at = datetime.now(timezone.utc)

                db.session.commit()
                db.session.refresh(session_entity)
                return UserSessionModel.model_validate(session_entity)

            except SQLAlchemyError:
                db.session.rollback()
                raise

    def revoke_all_user_sessions(
        self,
        user_id: str
    ) -> bool:
         with self.__connection_handler_factory() as db:
            try:
                updated_sessions = db.session.query(UsersSessionEntity) \
                    .filter(UsersSessionEntity.user_id == user_id) \
                    .update({ "revoked_at": datetime.now(timezone.utc)})

                db.session.commit()

                return updated_sessions > 0

            except SQLAlchemyError:
                db.session.rollback()
                raise

    def delete_expired_sessions(self) -> int:
        with self.__connection_handler_factory() as db:
            try:
                deleted_sessions = (
                    db.session.query(UsersSessionEntity)
                    .filter(
                        UsersSessionEntity.expires_at
                        <= datetime.now(timezone.utc)
                    )
                    .delete()
                )

                db.session.commit()
                return deleted_sessions

            except SQLAlchemyError:
                db.session.rollback()
                raise

    def delete_expired_sessions_by_user(self, user_id: str) -> int:
        with self.__connection_handler_factory() as db:
            try:
                deleted_sessions = (
                    db.session.query(UsersSessionEntity)
                    .filter(
                        UsersSessionEntity.expires_at
                        <= datetime.now(timezone.utc)
                    )
                    .where(UsersSessionEntity.user_id == user_id) \
                    .delete()
                )

                db.session.commit()
                return deleted_sessions

            except SQLAlchemyError:
                db.session.rollback()
                raise

    def select_session_by_id(
        self,
        session_id: str,
    ) -> UserSessionModel | None:
        with self.__connection_handler_factory() as db:
            try:
                session = (
                    db.session.query(UsersSessionEntity)
                    .filter(UsersSessionEntity.id == session_id)
                    .first()
                )

                if session is None:
                    return None

                return UserSessionModel.model_validate(session)

            except SQLAlchemyError:
                db.session.rollback()
                raise

    def select_session_by_user_id(
            self,
            user_id: str,
        ) -> UserSessionModel | None:
            with self.__connection_handler_factory() as db:
                try:
                    session = (
                        db.session.query(UsersSessionEntity)
                        .filter(UsersSessionEntity.user_id == user_id)
                        .first()
                    )
    
                    if session is None:
                        return None
    
                    return UserSessionModel.model_validate(session)
    
                except SQLAlchemyError:
                    db.session.rollback()
                    raise