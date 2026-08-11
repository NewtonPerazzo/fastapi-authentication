from collections.abc import Callable

from app.users.users_model import UsersModel
from app.users.users_entity import UsersEntity
from config.db_connection import DBConnectionHandler
from sqlalchemy.exc import SQLAlchemyError

class UsersRepository():
    def __init__(
        self,
        connection_handler_factory: Callable[[], DBConnectionHandler],
    ) -> None:
        self.__connection_handler_factory = connection_handler_factory

    def select_by_id(
        self,  
        user_id: str,
    ) -> UsersModel | None:
        with self.__connection_handler_factory() as db:
            try:
                user = db.session.query(UsersEntity)\
                    .filter(UsersEntity.id == user_id)\
                    .first()
                return UsersModel.model_validate(user) if user else None
            except SQLAlchemyError as error:
                db.session.rollback()
                raise

    def select_by_email(self, email: str) -> UsersModel | None:
        with self.__connection_handler_factory() as db:
            try:
                user = db.session.query(UsersEntity) \
                    .filter(UsersEntity.email == email) \
                    .first()
                return UsersModel.model_validate(user) if user else None
            except SQLAlchemyError:
                db.session.rollback()
                raise

    def select_by_phone(self, phone: str) -> UsersModel | None:
        with self.__connection_handler_factory() as db:
            try:
                user = db.session.query(UsersEntity) \
                    .filter(UsersEntity.phone == phone) \
                    .first()
                return UsersModel.model_validate(user) if user else None
            except SQLAlchemyError:
                db.session.rollback()
                raise

    def insert(
        self,  
        user: dict,
    ) -> UsersModel:
        with self.__connection_handler_factory() as db:
            try:
                user_entity = UsersEntity(**user)
                db.session.add(user_entity)
                db.session.commit()
                db.session.refresh(user_entity)
                return UsersModel.model_validate(user_entity)
            except SQLAlchemyError as error:
                db.session.rollback()
                raise

    def update(
        self,  
        user_id: str,
        user: dict,
    ) -> UsersModel | None:
        with self.__connection_handler_factory() as db:
            try:
                user_entity = db.session.query(UsersEntity) \
                    .filter(UsersEntity.id == user_id) \
                    .first()

                if user_entity is None:
                    return None

                for field, value in user.items():
                    setattr(user_entity, field, value)

                db.session.commit()
                db.session.refresh(user_entity)
                return UsersModel.model_validate(user_entity)

            except SQLAlchemyError:
                db.session.rollback()
                raise

    def change_activity(
        self,
        user_id: str,
        is_active: bool,
    ) -> UsersModel | None:
        return self.update(
            user_id=user_id,
            user={"is_active": is_active},
        )
        

    def delete(
        self,  
        user_id: str,
    ) -> bool:
        with self.__connection_handler_factory() as db:
            try:
                user_deleted = db.session.query(UsersEntity) \
                    .filter(
                        UsersEntity.id
                        == user_id
                    ) \
                    .delete()

                db.session.commit()
                return bool(user_deleted)

            except SQLAlchemyError:
                db.session.rollback()
                raise
