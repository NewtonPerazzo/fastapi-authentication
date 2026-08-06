from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
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
