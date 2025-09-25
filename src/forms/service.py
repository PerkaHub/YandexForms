from sqlalchemy.ext.asyncio import AsyncSession

from src.forms.schemas import CreateOrUpdateForm
from src.forms.repository import FormRepository
from src.exceptions import UnexpectedException, FormNotFoundExceprion


class FormService:
    @staticmethod
    async def get_or_not_found(session, form_id=None, user_id=None):
        if user_id and form_id:
            form = await FormRepository.get_one_or_none(
                session, id=form_id, owner_id=user_id)
            if not form:
                raise FormNotFoundExceprion()
        elif user_id and not form_id:
            forms = await FormRepository.get_all(session, owner_id=user_id)
            if not forms:
                raise FormNotFoundExceprion()
        else:
            form = await FormRepository.get_one_or_none(session, id=form_id)
            if not form:
                raise FormNotFoundExceprion()
        return form

    @staticmethod
    async def create_form(
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
        return await cls.get_or_not_found(session, form_id=form_id)

    @classmethod
    async def get_my_forms(cls, user_id: int, session: AsyncSession):
        return await cls.get_or_not_found(session, user_id=user_id)

    @classmethod
    async def update_form(
        cls,
        form_id: int,
        update_data: CreateOrUpdateForm,
        session: AsyncSession
    ):
        form = await cls.get_or_not_found(session, form_id=form_id)

        form.title = update_data.title
        form.description = update_data.description

        return await FormRepository.update_form(update_data, form, session)

    @classmethod
    async def delete_form(
        cls,
        form_id: int,
        user_id: int,
        session: AsyncSession
    ):
        form = await cls.get_or_not_found(
            session, form_id=form_id, user_id=user_id)
        await FormRepository.delete_form(form, session)
