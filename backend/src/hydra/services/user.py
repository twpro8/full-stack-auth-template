from hydra.exceptions import UserNotFoundError
from hydra.schemas import PaginatedResult
from hydra.schemas.user import User
from hydra.services import BaseService


class UserService(BaseService):
    async def get_all(self, offset: int, limit: int) -> PaginatedResult[User]:
        users = await self.uow.users.get_all(offset, limit)
        count = await self.uow.users.get_count()
        return PaginatedResult(items=users, count=count)

    async def get_by_id(self, user_id: int) -> User:
        user = await self.uow.users.get_by_id(user_id)
        if not user:
            raise UserNotFoundError
        return user
