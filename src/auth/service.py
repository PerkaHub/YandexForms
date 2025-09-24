from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import secrets

from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from src.auth.constants import (
    EXPIRES_DAYS_AT_REFRESH_TOKEN,
    EXPIRES_MINUTES_AT_ACCESS_TOKEN
)
from src.auth.repository import UserRepository
from src.auth.schemas import Tokens
from src.auth.repository import RefreshTokenRepository
from src.config import settings
from src.exceptions import (
    TokenExpiredException,
    InvalidTokenException,
    TokenNotFoundException,
    UsernameAlreadyExistsException,
    IncorrectUserDataException
)

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


class UserService:
    @classmethod
    async def register_user(cls, username, password, session):
        user = await UserRepository.get_one_or_none(session, username=username)
        if user:
            raise UsernameAlreadyExistsException()
        hashed_password = get_password_hash(password)
        await UserRepository.add_data(
            session=session,
            username=username,
            hashed_password=hashed_password
        )
        new_user = await UserRepository.get_one_or_none(
            session, username=username)
        if not new_user:
            raise ValueError("User creation failed")
        return await create_tokens(new_user.id, username, session)

    @classmethod
    async def login_user(cls, username, password, session):
        user = await UserRepository.get_one_or_none(session, username=username)
        if not user or not verify_password(password, user.hashed_password):
            raise IncorrectUserDataException()
        return await create_tokens(user.id, username, session)


async def create_access_token(
    user_id: int,
    username: str
) -> str:
    payload = {
        'sub': str(user_id),
        'username': str(username),
        'exp': datetime.now(timezone.utc)
        + timedelta(minutes=EXPIRES_MINUTES_AT_ACCESS_TOKEN)
    }
    try:
        encoded_jwt = jwt.encode(
            payload, settings.SECRET_KEY, settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        raise ValueError(f'failed to create access token: {e}')


async def create_or_update_refresh_token(
    user_id: int,
    session: AsyncSession
) -> str:
    original_token = secrets.token_urlsafe(64)

    hashed_token = get_password_hash(original_token)

    expires_at = (
        datetime.now() + timedelta(days=EXPIRES_DAYS_AT_REFRESH_TOKEN)
    )
    created_at = datetime.now()
    await RefreshTokenRepository.delete_data(session, user_id=user_id)

    await RefreshTokenRepository.add_data(
        session=session,
        user_id=user_id,
        token_hash=hashed_token,
        expires_at=expires_at,
        created_at=created_at
    )

    return original_token


async def create_tokens(id, username, session) -> Tokens:
    refresh_token = await create_or_update_refresh_token(id, session)
    access_token = await create_access_token(id, username)
    return Tokens(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def refresh_access_token(refresh_token: str | None, session) -> Tokens:
    if not refresh_token:
        raise TokenNotFoundException()

    refresh_token_record = await RefreshTokenRepository.get_refresh_token(
        refresh_token, session
    )

    if not refresh_token_record:
        raise InvalidTokenException()

    if refresh_token_record.expires_at < datetime.now():
        await RefreshTokenRepository.delete_data(
            session, id=refresh_token_record.id
        )
        raise TokenExpiredException()

    user = await UserRepository.get_one_or_none(
        session, id=refresh_token_record.user_id)
    if not user:
        raise InvalidTokenException()

    tokens = await create_tokens(user.id, user.username, session)
    return Tokens(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token
    )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
