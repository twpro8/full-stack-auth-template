from typing import Sequence

from hydra.exceptions import UserNotFoundError
from hydra.schemas.user import User
from hydra.services import BaseService


class UserService(BaseService):
    async def get_all(self) -> tuple[Sequence[User], int]:
        users = await self.uow.users.get_all()
        count = 123  # TODO: get users count from db
        return users, count

    async def get_by_id(self, user_id: int) -> User:
        user = await self.uow.users.get_by_id(user_id)
        if not user:
            raise UserNotFoundError
        return user
