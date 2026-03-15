from datetime import datetime, timezone, timedelta

from hydra.config import settings
from hydra.errors import UserNotFoundError, InvalidPasswordError
from hydra.errors.auth import InvalidRefreshTokenError, RefreshTokenRevokedError
from hydra.models import RefreshTokenOrm
from hydra.schemas import TokenPair
from hydra.schemas.auth import AuthResult
from hydra.schemas.user import UserCreate
from hydra.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
)
from hydra.services import BaseService


class AuthService(BaseService):
    async def register(
        self,
        password: str,
        email: str,
        full_name: str,
    ) -> None:
        data_ = UserCreate(
            password_hash=hash_password(password),
            email=email,
            full_name=full_name,
        )
        await self.uow.users.create(data_)
        await self.uow.commit()

    async def login(self, email: str, password: str) -> AuthResult:
        user = await self.uow.users.get_by_email(email)
        if not user:
            raise UserNotFoundError
        if not verify_password(user.password_hash, password):
            raise InvalidPasswordError
        tokens = await self._issue_token(user.id)
        await self.uow.commit()
        return AuthResult(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            user=user,
        )

    async def refresh(self, refresh_token: str) -> TokenPair:
        stored = await self._get_valid_refresh_token(refresh_token)
        # Refresh Token Rotation
        await self.uow.refresh_tokens.revoke(stored.id)
        tokens = await self._issue_token(stored.user_id)
        await self.uow.commit()
        return tokens

    async def logout(self, refresh_token: str) -> None:
        try:
            stored = await self._get_valid_refresh_token(refresh_token)
        except InvalidRefreshTokenError, RefreshTokenRevokedError:
            return
        await self.uow.refresh_tokens.revoke(stored.id)
        await self.uow.commit()

    async def _issue_token(self, user_id: int) -> TokenPair:
        access_token = create_access_token(user_id)
        refresh_token, refresh_token_hash = create_refresh_token()
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        await self.uow.refresh_tokens.create(user_id, refresh_token_hash, expires_at)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def _get_valid_refresh_token(self, refresh_token: str) -> RefreshTokenOrm:
        token_hash = hash_refresh_token(refresh_token)
        stored = await self.uow.refresh_tokens.get_by_token_hash(token_hash)
        if not stored or stored.expires_at <= datetime.now(timezone.utc):
            raise InvalidRefreshTokenError
        if stored.is_revoked:
            # Reuse detected — potential token theft, revoke all user sessions
            await self.uow.refresh_tokens.revoke_all(stored.user_id)
            await self.uow.commit()
            raise RefreshTokenRevokedError
        return stored
