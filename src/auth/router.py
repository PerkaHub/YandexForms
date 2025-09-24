from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.auth.schemas import TokenInfo, UserCreate
from src.auth.service import UserService
from src.auth.cookies import set_refresh_cookie
from src.auth.service import refresh_access_token


router = APIRouter(
    prefix='/api/v1/auth',
    tags=['Authentification']
)


@router.post('/register')
async def register_user(
    response: Response,
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db_session),
) -> TokenInfo:
    tokens = await UserService.register_user(
        username=user_data.username,
        password=user_data.password,
        session=session
    )
    set_refresh_cookie(response, tokens.refresh_token)
    return TokenInfo(
        access_token=tokens.access_token,
        token_type='Bearer'
    )


@router.post('/login')
async def login_user(
    response: Response,
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db_session),
) -> TokenInfo:
    tokens = await UserService.login_user(
        username=user_data.username,
        password=user_data.password,
        session=session
    )
    set_refresh_cookie(response, tokens.refresh_token)
    return TokenInfo(
        access_token=tokens.access_token,
        token_type='Bearer'
    )


@router.post("/refresh")
async def refresh(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db_session),
) -> TokenInfo:
    refresh_token = request.cookies.get("refresh_token")
    tokens = await refresh_access_token(refresh_token, session)
    set_refresh_cookie(response, tokens.refresh_token)
    return TokenInfo(
        access_token=tokens.access_token,
        token_type='Bearer'
    )
