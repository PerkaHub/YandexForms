from sqlalchemy.ext.asyncio import AsyncSession

from src.forms.schemas import CreateOrUpdateForm
from src.forms.repository import FormRepository
from src.exceptions import UnexpectedException, FormNotFoundExceprion


class FormService:
    @classmethod
    async def create_form(
        cls,
        data: CreateOrUpdateForm,
        user_id: int,
        session: AsyncSession
    ):
        try:
            return await FormRepository.add_form(data, user_id, session)
        except Exception:
            raise UnexpectedException()

    @classmethod
    async def get_forms(cls, form_id: int, session: AsyncSession):
        form = await FormRepository.get_one_or_none(session, id=form_id)
        if not form:
            raise FormNotFoundExceprion()
        return form

    @classmethod
    async def get_my_forms(cls, user_id: int, session: AsyncSession):
        forms = await FormRepository.get_all(session, owner_id=user_id)
        if not forms:
            raise FormNotFoundExceprion()
        return forms

    @classmethod
    async def update_form(
        cls,
        form_id: int,
        update_data: CreateOrUpdateForm, 
        session: AsyncSession
    ):
        form = await FormRepository.get_one_or_none(session, id=form_id)
        if not form:
            raise FormNotFoundExceprion()

        form.title = update_data.title
        form.description = update_data.description

        return await FormRepository.update_form(update_data, form, session)
