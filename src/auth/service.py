from passlib.context import CryptContext

from src.auth.tokens import create_access_token
from src.auth.repository import UserRepository

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


class UsernameAlreadyExistsError(Exception):
    pass


class IncorrectUserData(Exception):
    pass


class UserService:
    @classmethod
    async def register_user(cls, username, password, session):
        user = await UserRepository.get_one_or_none(session, username=username)
        if user:
            raise UsernameAlreadyExistsError(f"User with username {username} already exists")
        hashed_password = get_password_hash(password)
        await UserRepository.add_data(
            session=session,
            username=username,
            hashed_password=hashed_password
        )
        new_user = await UserRepository.get_one_or_none(session, username=username)
        if not new_user:
            raise ValueError("User creation failed")
        return await create_access_token(new_user.id, username)

    @classmethod
    async def login_user(cls, username, password, session):
        user = await UserRepository.get_one_or_none(session, username=username)
        if not user or not verify_password(password, user.hashed_password):
            raise IncorrectUserData('incorrect username or password')
        return await create_access_token(user.id, username)
    

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
