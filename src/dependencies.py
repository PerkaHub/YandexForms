from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repository import UserRepository
from src.config import settings
from src.database import get_db_session


security = HTTPBearer()


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except PyJWTError:
        raise credentials_exception
    

async def get_current_user(
    payload: dict = Depends(verify_token),
    session: AsyncSession = Depends(get_db_session)
):
    user = await UserRepository.get_one_or_none(session, username=payload.get('username'))
    if user is None:
        raise credentials_exception
    
    return user
