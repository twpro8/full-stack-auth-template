from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hydra.database import get_session
from hydra.database.unit_of_work import UnitOfWork
from hydra.services import AuthService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_unit_of_work(session: SessionDep) -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(session) as unit_of_work:
        yield unit_of_work


UnitOfWorkDep = Annotated[UnitOfWork, Depends(get_unit_of_work)]


def get_auth_service(unit_of_work: UnitOfWorkDep) -> AuthService:
    return AuthService(unit_of_work)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
