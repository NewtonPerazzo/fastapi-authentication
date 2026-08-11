import re

from pwdlib import PasswordHash

from config.db_dependencies import get_connection_handler
from app.exceptions.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.users.users_repository import UsersRepository
from app.users.users_model import UsersModel, UsersRequestModel, UsersUpdateModel
from datetime import datetime, timezone

class UsersService():
    def __init__(self) -> None:
        self._users_repository = UsersRepository(
            connection_handler_factory=get_connection_handler,
        )
        self._password_hash = PasswordHash.recommended()

    def get_user(
            self,  
            user_id: str,
        ) -> UsersModel:
        response = self._users_repository.select_by_id(user_id=user_id)
        if response is None:
            raise UserNotFoundException(user_id=str(user_id))
        return response

    def get_user_by_email(
            self,  
            email: str,
        ) -> UsersModel:
        response = self._users_repository.select_by_email(email=email)
        if response is None:
            raise UserNotFoundException(user=str(email))
        return response

    def post_user(
            self,  
            user: UsersRequestModel,
        ) -> UsersModel:
        user_normalized = self.normalize_user(user=user)

        if self._users_repository.select_by_email(user_normalized["email"]):
            raise UserAlreadyExistsException(field="email")

        if self._users_repository.select_by_phone(user_normalized["phone"]):
            raise UserAlreadyExistsException(field="phone")

        response = self._users_repository.insert(user=user_normalized)
        return response

    def reset_password(
        self,
        user_id: str,
        new_password: str,
    ) -> UsersModel:
        self.get_user(user_id=user_id)

        now = datetime.now(timezone.utc)
        user_data = {
            "password_hash": self.get_hash_pass(new_password),
            "updated_at": now,
            "password_changed_at": now,
        }

        response = self._users_repository.update(
            user_id=user_id,
            user=user_data,
        )

        if response is None:
            raise UserNotFoundException(user=user_id)

        return response

    def update_user(
            self,  
            user_id: str,
            user: UsersUpdateModel,
        ) -> UsersModel:
        current_user = self.get_user(user_id=user_id)
        user_normalized = self.normalize_user_update(user=user)

        if not user_normalized:
            return current_user

        email = user_normalized.get("email")
        if email:
            user_with_email = self._users_repository.select_by_email(email)
            if user_with_email and user_with_email.id != user_id:
                raise UserAlreadyExistsException(field="email")

        phone = user_normalized.get("phone")
        if phone:
            user_with_phone = self._users_repository.select_by_phone(phone)
            if user_with_phone and user_with_phone.id != user_id:
                raise UserAlreadyExistsException(field="phone")

        response = self._users_repository.update(
            user_id=user_id,
            user=user_normalized,
        )
        if response is None:
            raise UserNotFoundException(user_id=str(user_id))
        return response

    def delete_user(
            self,  
            user_id: str,
        ) -> bool:
        response = self._users_repository.delete(user_id=user_id)
        if not response:
            raise UserNotFoundException(user_id=str(user_id))
        return response

    def change_user_activity(
        self,
        user_id: str,
        is_active: bool,
    ) -> UsersModel:
        response = self._users_repository.change_activity(
            user_id=user_id,
            is_active=is_active,
        )
        if response is None:
            raise UserNotFoundException(user_id=str(user_id))
        return response

    def normalize_user(
        self,
        user: UsersRequestModel,
    ) -> dict:
        return {
            "email": user.email.strip().lower(),
            "first_name": " ".join(user.first_name.strip().split()),
            "last_name": " ".join(user.last_name.strip().split()),
            "phone": re.sub(r"\D", "", user.phone),
            "password_hash": self.get_hash_pass(user.password),
        }

    def normalize_user_update(self, user: UsersUpdateModel) -> dict:
        user_data = user.model_dump(exclude_none=True)

        if "email" in user_data:
            user_data["email"] = user_data["email"].strip().lower()
        if "first_name" in user_data:
            user_data["first_name"] = " ".join(
                user_data["first_name"].strip().split()
            )
        if "last_name" in user_data:
            user_data["last_name"] = " ".join(
                user_data["last_name"].strip().split()
            )
        if "phone" in user_data:
            user_data["phone"] = re.sub(r"\D", "", user_data["phone"])

        return user_data

    def get_hash_pass(
        self,
        password: str,
    ) -> str:
        return self._password_hash.hash(password)

    def verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        return self._password_hash.verify(password, password_hash)
    
users_service = UsersService()
