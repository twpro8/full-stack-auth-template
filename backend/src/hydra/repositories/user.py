from typing import Sequence

from sqlalchemy import insert, select

from hydra.models import UserOrm
from hydra.repositories import BaseRepository
from hydra.schemas.user import UserCreate, User


class UserRepository(BaseRepository):
    async def create(self, data: UserCreate) -> None:
        statement = insert(UserOrm).values(data.model_dump())
        await self.session.execute(statement)

    async def get_all(self) -> Sequence[User]:
        query = select(UserOrm)
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
