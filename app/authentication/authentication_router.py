from fastapi import APIRouter, Depends, Response, status
from app.authentication.authentication_model import (
    LoginRequestModel,
    RefreshTokenRequestModel,
    ResetPasswordBodyModel,
    TokenResponseModel,
)
from app.authentication.services.authentication_service import (
    authentication_service,
)

authentication_router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"]
)

@authentication_router.post(
    "/login",
    response_model=TokenResponseModel,
)
def login(
    login_data: LoginRequestModel,
) -> TokenResponseModel:
    return authentication_service.login(
        login_data=login_data,
    )

@authentication_router.post(
    "/refresh",
    response_model=TokenResponseModel,
)
def refresh(
    refresh_data: RefreshTokenRequestModel,
) -> TokenResponseModel:
    return authentication_service.refresh(
        refresh_data=refresh_data,
    )


@authentication_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    refresh_data: RefreshTokenRequestModel,
) -> Response:
    authentication_service.logout(
        refresh_data=refresh_data,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )

@authentication_router.post(
    "/reset-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def reset_password(
    reset_password_data: ResetPasswordBodyModel,
) -> Response:
    authentication_service.reset_password(
        reset_password_data=reset_password_data,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
    
