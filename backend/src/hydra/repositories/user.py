from typing import Sequence

from asyncpg.exceptions import UniqueViolationError  # type: ignore[import-untyped]
from sqlalchemy import insert, select, func
from sqlalchemy.exc import IntegrityError

from hydra.exceptions import UsernameAlreadyExistsError, EmailAlreadyExistsError
from hydra.models import UserOrm
from hydra.repositories import BaseRepository
from hydra.schemas.user import UserCreate, User


class UserRepository(BaseRepository):
    async def create(self, data: UserCreate) -> None:
        statement = insert(UserOrm).values(data.model_dump())
        try:
            await self.session.execute(statement)
        except IntegrityError as e:
            cause = getattr(e.orig, "__cause__", None)
            constraint = getattr(cause, "constraint_name", None)
            if isinstance(cause, UniqueViolationError):
                match constraint:
                    case "users_username_key":
                        raise UsernameAlreadyExistsError from e
                    case "users_email_key":
                        raise EmailAlreadyExistsError from e
                    case _:
                        raise
            raise

    async def get_all(self, offset: int, limit: int) -> Sequence[User]:
        query = select(UserOrm).offset(offset).limit(limit)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [User.model_validate(model) for model in models]

    async def get_by_id(self, user_id: int) -> User | None:
        user = await self.session.get(UserOrm, user_id)

        if user is None:
            return None

        return User.model_validate(user)

    async def get_by_username(self, username: str) -> User | None:
        query = select(UserOrm).filter_by(username=username)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            return None

        return User.model_validate(user)

    async def get_count(self) -> int:
        query = select(func.count()).select_from(UserOrm)
        result = await self.session.execute(query)
        return result.scalar_one()
