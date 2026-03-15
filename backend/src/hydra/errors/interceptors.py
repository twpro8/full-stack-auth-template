from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from hydra.errors import (
    HydraError,
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    InvalidPasswordError,
)
from hydra.errors.auth import InvalidRefreshTokenError, RefreshTokenRevokedError

_DEFAULT = (status.HTTP_500_INTERNAL_SERVER_ERROR, "Unexpected error.")
errors: dict[type[HydraError], tuple[int, str]] = {
    HydraError: _DEFAULT,
    InvalidPasswordError: (
        status.HTTP_401_UNAUTHORIZED,
        "Incorrect password",
    ),
    InvalidCredentialsError: (
        status.HTTP_403_FORBIDDEN,
        "Could not validate credentials",
    ),
    UserNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "User not found",
    ),
    UserAlreadyExistsError: (
        status.HTTP_409_CONFLICT,
        "User already exists",
    ),
    InvalidRefreshTokenError: (
        status.HTTP_401_UNAUTHORIZED,
        "Invalid refresh token",
    ),
    RefreshTokenRevokedError: (
        status.HTTP_401_UNAUTHORIZED,
        "Refresh token has been revoked",
    ),
}


async def app_exception_handler(_: Request, e: HydraError) -> JSONResponse:
    status_code, detail = errors.get(type(e), _DEFAULT)
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail},
    )
