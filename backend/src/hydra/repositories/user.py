from sqlalchemy import insert, select

from hydra.models import UserOrm
from hydra.repositories import BaseRepository
from hydra.schemas.user import UserCreate, User


class UserRepository(BaseRepository):
    async def create(self, data: UserCreate) -> None:
        statement = insert(UserOrm).values(data.model_dump())
        await self.session.execute(statement)

    async def get_by_username(self, username: str) -> User | None:
        query = select(UserOrm).filter_by(username=username)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            return None

        return User.model_validate(user, from_attributes=True)
