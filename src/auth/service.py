from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import secrets

from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from jwt import PyJWTError

from src.auth.constants import (
    EXPIRES_DAYS_AT_REFRESH_TOKEN,
    EXPIRES_MINUTES_AT_ACCESS_TOKEN
)
from src.auth.repository import UserRepository
from src.auth.schemas import Tokens
from src.auth.repository import RefreshTokenRepository
from src.config import settings

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


class UsernameAlreadyExistsError(Exception):
    pass


class IncorrectUserData(Exception):
    pass


class TokenNotFound(Exception):
    pass


class InvalidToken(Exception):
    pass


class TokenExpired(Exception):
    pass


class UserService:
    @classmethod
    async def register_user(cls, username, password, session):
        user = await UserRepository.get_one_or_none(session, username=username)
        if user:
            raise UsernameAlreadyExistsError(
                f"User with username {username} already exists"
            )
        hashed_password = get_password_hash(password)
        await UserRepository.add_data(
            session=session,
            username=username,
            hashed_password=hashed_password
        )
        new_user = await UserRepository.get_one_or_none(session, username=username)
        if not new_user:
            raise ValueError("User creation failed")
        return await create_tokens(new_user.id, username, session)

    @classmethod
    async def login_user(cls, username, password, session):
        user = await UserRepository.get_one_or_none(session, username=username)
        if not user or not verify_password(password, user.hashed_password):
            raise IncorrectUserData('incorrect username or password')
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
    try:
        if not refresh_token:
            raise TokenNotFound('Refresh token not found')

        refresh_token_record = await RefreshTokenRepository.get_refresh_token(
            refresh_token, session
        )

        if not refresh_token_record:
            raise InvalidToken('Invalid refresh token')

        if refresh_token_record.expires_at < datetime.now():
            await RefreshTokenRepository.delete_data(
                session, id=refresh_token_record.id
            )
            raise TokenExpired('Refresh token expired')

        user = await UserRepository.get_one_or_none(
            session, id=refresh_token_record.user_id)
        if not user:
            raise InvalidToken('User not found')

        tokens = await create_tokens(user.id, user.username, session)
        return Tokens(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token
        )

    except (TokenNotFound, TokenExpired, InvalidToken) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation error"
        )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
