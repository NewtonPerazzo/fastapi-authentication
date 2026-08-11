from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    InvalidRefreshTokenException,
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    InactiveUserException,
    RefreshTokenExpiredException,
    AccessTokenExpiredException,
    InvalidAccessTokenException,
    SessionRevokedException
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(
        request: Request,
        exception: UserNotFoundException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "error": "user_not_found",
                "message": str(exception),
            },
        )

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_handler(
        request: Request,
        exception: UserAlreadyExistsException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "error": "user_already_exists",
                "message": str(exception),
            },
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(
        request: Request,
        exception: InvalidCredentialsException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={
                "error": "invalid_credentials",
                "message": str(exception),
            },
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    @app.exception_handler(InactiveUserException)
    async def inactive_user_handler(
        request: Request,
        exception: InactiveUserException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=403,
            content={
                "error": "inactive_user",
                "message": str(exception),
            },
        )

    @app.exception_handler(AccessTokenExpiredException)
    async def access_token_expired_handler(
        request: Request,
        exception: AccessTokenExpiredException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={
                "error": "access_token_expired",
                "message": str(exception),
            },
            headers={"WWW-Authenticate": "Bearer"},
        )


    @app.exception_handler(InvalidAccessTokenException)
    async def invalid_access_token_handler(
        request: Request,
        exception: InvalidAccessTokenException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={
                "error": "invalid_access_token",
                "message": str(exception),
            },
            headers={"WWW-Authenticate": "Bearer"},
        )


    @app.exception_handler(InvalidRefreshTokenException)
    async def invalid_refresh_token_handler(
        request: Request,
        exception: InvalidRefreshTokenException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={
                "error": "invalid_refresh_token",
                "message": str(exception),
            },
        )


    @app.exception_handler(RefreshTokenExpiredException)
    async def refresh_token_expired_handler(
        request: Request,
        exception: RefreshTokenExpiredException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={
                "error": "refresh_token_expired",
                "message": str(exception),
            },
        )


    @app.exception_handler(SessionRevokedException)
    async def session_revoked_handler(
        request: Request,
        exception: SessionRevokedException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={
                "error": "session_revoked",
                "message": str(exception),
            },
        )
