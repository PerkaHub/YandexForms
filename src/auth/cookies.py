from fastapi import Response

from src.auth.constants import EXPIRES_DAYS_AT_REFRESH_TOKEN


def set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=EXPIRES_DAYS_AT_REFRESH_TOKEN * 60 * 60 * 24,
    )
