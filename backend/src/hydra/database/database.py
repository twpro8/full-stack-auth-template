from typing import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from hydra.config import settings

# TODO: configure pool size and max_overflow
engine = create_async_engine(str(settings.DB_URL))
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with sessionmaker() as session:
        yield session


class Base(DeclarativeBase):
    pass
