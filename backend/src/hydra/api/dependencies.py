from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from sqlalchemy.ext.asyncio import AsyncSession

from hydra.database import get_session
from hydra.database.unit_of_work import UnitOfWork
from hydra.schemas.auth import TokenPayload
from hydra.schemas.common import PaginationParams
from hydra.schemas.user import User
from hydra.security import decode_access_token
from hydra.services import AuthService, UserService

access_cookie_scheme = APIKeyCookie(name="access_token", auto_error=False)
refresh_cookie_scheme = APIKeyCookie(name="refresh_token", auto_error=False)
SessionDep = Annotated[AsyncSession, Depends(get_session)]
PaginationDep = Annotated[PaginationParams, Depends()]


def get_access_token_cookie(
    token: Annotated[str | None, Depends(access_cookie_scheme)],
) -> str:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "APIKey"},
        )
    return token


AccessTokenDep = Annotated[str, Depends(get_access_token_cookie)]
RefreshTokenOptionalDep = Annotated[str | None, Depends(refresh_cookie_scheme)]


def get_refresh_token_cookie(token: RefreshTokenOptionalDep) -> str:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "APIKey"},
        )
    return token


RefreshTokenDep = Annotated[str, Depends(get_refresh_token_cookie)]


def require_not_authenticated(
    token: Annotated[str | None, Depends(access_cookie_scheme)],
) -> None:
    if token is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Already authenticated",
        )


async def get_unit_of_work(session: SessionDep) -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(session) as unit_of_work:
        yield unit_of_work


UnitOfWorkDep = Annotated[UnitOfWork, Depends(get_unit_of_work)]


def get_auth_service(unit_of_work: UnitOfWorkDep) -> AuthService:
    return AuthService(unit_of_work)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_user_service(unit_of_work: UnitOfWorkDep) -> UserService:
    return UserService(unit_of_work)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user_id(token: AccessTokenDep) -> int:
    payload = decode_access_token(token)
    token_data = TokenPayload(**payload)
    return token_data.sub


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_current_user(
    user_id: UserIdDep,
    service: UserServiceDep,
) -> User:
    user = await service.get_by_id(user_id)
    return user


UserDep = Annotated[User, Depends(get_current_user)]


async def get_current_superuser(current_user: UserDep) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform this action",
        )
    return current_user
