from sqlalchemy.ext.asyncio import AsyncSession

from src.forms.schemas import CreateForm
from src.forms.repository import FormRepository
from src.exceptions import UnexpectedException


class FormService:
    @classmethod
    async def create_form(
        cls,
        data: CreateForm,
        user_id: int,
        session: AsyncSession
    ):
        try:
            return await FormRepository.add_form(data, user_id, session)
        except Exception:
            raise UnexpectedException()
