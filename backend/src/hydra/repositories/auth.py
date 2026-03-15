from datetime import datetime

from sqlalchemy import select, update

from hydra.models import RefreshTokenOrm
from hydra.repositories import BaseRepository


class RefreshTokenRepository(BaseRepository):
    async def create(self, user_id: int, token_hash: str, expires_at: datetime) -> None:
        token = RefreshTokenOrm(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.session.add(token)
        await self.session.flush()

    async def get_by_token_hash(self, token_hash: str) -> RefreshTokenOrm | None:
        query = select(RefreshTokenOrm).filter_by(token_hash=token_hash)
        result = await self.session.execute(query)
        token = result.scalar_one_or_none()
        return token

    async def revoke(self, token_id: int) -> None:
        statement = (
            update(RefreshTokenOrm).filter_by(id=token_id).values({"is_revoked": True})
        )
        await self.session.execute(statement)

    async def revoke_all(self, user_id: int) -> None:
        statement = (
            update(RefreshTokenOrm)
            .filter_by(user_id=user_id, is_revoked=False)
            .values({"is_revoked": True})
        )
        await self.session.execute(statement)
