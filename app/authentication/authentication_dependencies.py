from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.authentication.services.authentication_service import (
    authentication_service,
)
from app.exceptions.exceptions import (
    InactiveUserException,
    InvalidAccessTokenException,
    UserNotFoundException,
)
from app.users.users_model import UsersModel
from app.users.users_service import users_service


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
) -> UsersModel:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise InvalidAccessTokenException()

    payload = authentication_service.validate_access_token(
        access_token=credentials.credentials,
    )

    try:
        user = users_service.get_user(user_id=payload.sub)
    except UserNotFoundException as error:
        raise InvalidAccessTokenException() from error

    if not user.is_active:
        raise InactiveUserException()

    return user
