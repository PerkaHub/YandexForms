from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.base import BaseRepository
from src.users.models import User, RefreshToken


class UserRepository(BaseRepository[User]):
    model = User


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    model = RefreshToken

    @classmethod
    async def get_refresh_token(
        cls, refresh_token: str, session: AsyncSession
    ):
        time_limit = datetime.now() - timedelta(days=30)

        query = select(RefreshToken).where(
            RefreshToken.expires_at > datetime.now(),
            RefreshToken.created_at > time_limit
        )
        tokens = (await session.execute(query)).scalars().all()

        from src.auth.service import verify_password

        for token_record in tokens:
            if verify_password(refresh_token, token_record.token_hash):
                return token_record
        return None
