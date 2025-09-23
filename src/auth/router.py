from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.auth.schemas import TokenInfo, UserCreate
from src.auth.service import UserService


router = APIRouter(
    prefix='/api/v1/auth',
    tags=['Authentification']
)


@router.post('/register')
async def register_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db_session),
) -> TokenInfo:
    access_token = await UserService.register_user(
        username=user_data.username,
        password=user_data.password,
        session=session
    )
    return TokenInfo(
        access_token=access_token,
        token_type='Bearer'
    )


@router.post('/login')
async def login_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db_session),
) -> TokenInfo:
    access_token = await UserService.login_user(
        username=user_data.username,
        password=user_data.password,
        session=session
    )
    return TokenInfo(
        access_token=access_token,
        token_type='Bearer'
    )
