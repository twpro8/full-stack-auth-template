from typing import Annotated, AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from hydra.config import settings
from hydra.database import get_session
from hydra.database.unit_of_work import UnitOfWork
from hydra.schemas.auth import TokenPayload
from hydra.security import decode_access_token
from hydra.services import AuthService, UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

TokenDep = Annotated[str, Depends(oauth2_scheme)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]


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


async def get_current_user_id(token: TokenDep) -> int:
    payload = decode_access_token(token)
    token_data = TokenPayload(**payload)
    return token_data.sub


UserIdDep = Annotated[int, Depends(get_current_user_id)]
