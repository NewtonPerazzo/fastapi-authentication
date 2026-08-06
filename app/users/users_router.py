from fastapi import APIRouter
from app.users.users_service import users_service
from app.users.users_model import (
    UserActivityModel,
    UsersModel,
    UsersRequestModel,
    UsersUpdateModel,
)

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@users_router.get(
        "/{user_id}",
        response_model=UsersModel
    )
def get_user(
    user_id: str,
):  
    response = users_service.get_user(user_id=user_id)
    return response

@users_router.post(
    "",
    response_model=UsersModel
)
def post_user(
    user_request: UsersRequestModel,
):  
    response = users_service.post_user(user=user_request)
    return response

@users_router.patch(
    "",
    response_model=UsersModel
)
def update_user(
    user_id: str,
    user_request: UsersUpdateModel,
):  
    response = users_service.update_user(
        user_id=user_id,
        user=user_request,
    )
    return response

@users_router.delete(
    "/{user_id}"
)
def delete_user(
    user_id: str,
):  
    response = users_service.delete_user(user_id=user_id)
    return response

@users_router.patch(
    "/{user_id}/activity",
    response_model=UsersModel
)
def change_user_activity(
    user_id: str,
    activity: UserActivityModel,
):  
    response = users_service.change_user_activity(
        user_id=user_id,
        is_active=activity.is_active,
    )
    return response
