from sqlalchemy.ext.asyncio import AsyncSession

from src.forms.models import FormField
from src.forms.schemas import AnswerData, CreateOrUpdateForm
from src.forms.repository import (
    FormRepository,
    FormFieldRepository,
    FormResponseRepository,
    FieldOptionRepository
)
from src.exceptions import (
    FieldNotFoundException,
    RequiredFieldException,
    UnexpectedException,
    FormNotFoundExceprion,
    TextAnswerRequiredException,
    OptionIDNotAllowedException,
    OptionIDRequiredException,
    OptionNotFoundException,
    TextNotAllowedException
)
from src.forms.utils import generate_response_id


class FormService:
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

    @staticmethod
    async def get_forms(form_id: int, session: AsyncSession):
        form = await FormRepository.get_one_or_none(session, id=form_id)
        if not form:
            raise FormNotFoundExceprion()
        return form

    @staticmethod
    async def get_my_forms(user_id: int, session: AsyncSession):
        forms = await FormRepository.get_all(session, owner_id=user_id)
        if not forms:
            raise FormNotFoundExceprion()
        return forms

    @staticmethod
    async def update_form(
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

    @staticmethod
    async def delete_form(
        form_id: int,
        user_id: int,
        session: AsyncSession
    ):
        form = await FormRepository.get_one_or_none(
                session, id=form_id, owner_id=user_id
            )
        if not form:
            raise FormNotFoundExceprion()
        await FormRepository.delete_form(form, session)


class FormResponseService:
    @classmethod
    async def submit_response(
        cls,
        form_id: int,
        user_id: int,
        answers: list[AnswerData],
        session: AsyncSession
    ):
        form = await FormRepository.get_one_or_none(session, id=form_id)
        if not form:
            raise FormNotFoundExceprion()

        response_id = await generate_response_id()

        answers_by_field_id = {answer.field_id: answer for answer in answers}

        await cls._validate_required_fields(
            form.fields, answers_by_field_id
        )

        for answer in answers:
            field = await FormFieldRepository.get_one_or_none(
                session, id=answer.field_id, form_id=form_id
            )
            if not field:
                raise FieldNotFoundException(answer.field_id)

            await cls._validate_answer(field, answer, session)

            await FormResponseRepository.add_data(
                session=session,
                response_id=response_id,
                form_id=form_id,
                field_id=answer.field_id,
                user_id=user_id,
                answer_text=answer.answer_text,
                answer_option_id=answer.answer_option_id
            )
        return response_id

    @classmethod
    async def _validate_required_fields(
        cls,
        fields: list[FormField],
        answers_by_field_id: dict[int, AnswerData]
    ):
        for field in fields:
            if field.is_required:
                answer = answers_by_field_id.get(field.id)

                if not answer or not cls._is_answer_provided(answer):
                    raise RequiredFieldException(field.question_text, field.id)

    @staticmethod
    async def _is_answer_provided(answer: AnswerData) -> bool:
        if answer.answer_text and answer.answer_text.strip():
            return True
        if answer.answer_option_id:
            return True
        return False

    @classmethod
    async def _validate_answer(
        cls,
        field: FormField,
        answer: AnswerData,
        session: AsyncSession
    ):
        if not field.is_required and not cls._is_answer_provided(answer):
            return

        if field.field_type in ['text']:
            if not answer.answer_text:
                raise TextAnswerRequiredException(field.id)

            if answer.answer_option_id:
                raise OptionIDNotAllowedException(field.id)

        elif field.field_type in ['radio', 'checkbox']:
            if not answer.answer_option_id:
                raise OptionIDRequiredException(field.id)

            if answer.answer_text:
                raise TextNotAllowedException(field.field_type, field.id)

            option = await FieldOptionRepository.get_one_or_none(
                session, id=answer.answer_option_id, field_id=field.id
            )
            if not option:
                raise OptionNotFoundException(
                    answer.answer_option_id, field.id
                )
