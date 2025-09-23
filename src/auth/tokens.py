from datetime import datetime, timedelta, timezone

import jwt

from src.auth.constants import EXPIRES_AT_ACCESS_TOKEN
from src.config import settings


async def create_access_token(
    user_id: int,
    username: str
) -> str:
    payload = {
        'sub': str(user_id),
        'username': str(username),
        'exp': datetime.now(timezone.utc)
        + timedelta(minutes=EXPIRES_AT_ACCESS_TOKEN)
    }
    try:
        encoded_jwt = jwt.encode(
            payload, settings.SECRET_KEY, settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        raise ValueError(f'failed to create access token: {e}')
