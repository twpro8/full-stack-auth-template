from hydra.exceptions import UserNotFoundError, InvalidPasswordError
from hydra.schemas.user import UserCreate
from hydra.security import hash_password, verify_password, create_access_token
from hydra.services import BaseService


class AuthService(BaseService):
    async def register(
        self,
        username: str,
        password: str,
        email: str,
        full_name: str,
    ) -> None:
        data_ = UserCreate(
            username=username,
            password_hash=hash_password(password),
            email=email,
            full_name=full_name,
        )
        await self.uow.users.create(data_)
        await self.uow.commit()

    async def login(self, username: str, password: str) -> str:
        user = await self.uow.users.get_by_username(username)
        if not user:
            raise UserNotFoundError
        if not verify_password(user.password_hash, password):
            raise InvalidPasswordError
        access_token = create_access_token(user.id)
        return access_token
