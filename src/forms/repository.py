from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from src.repository.base import BaseRepository
from src.forms.models import Form, FormField, FieldOption
from src.exceptions import DatabaseException


class FormRepository(BaseRepository[Form]):
    model = Form

    @staticmethod
    async def add_fields_and_options(data, form, session):
        form_fields_data = []
        for field_data in data.fields:
            form_fields_data.append({
                'form_id': form.id,
                'field_type': field_data.field_type.value,
                'question_text': field_data.question_text,
                'is_required': field_data.is_required
            })

        if form_fields_data:
            await session.execute(insert(FormField), form_fields_data)
            await session.flush()

        result = await session.execute(
            select(FormField.id).where(FormField.form_id == form.id)
        )
        field_ids = [row[0] for row in result]

        field_options_data = []
        for field_id, field_data in zip(field_ids, data.fields):
            for option_data in field_data.options:
                field_options_data.append({
                    'field_id': field_id,
                    'option_text': option_data.option_text
                })

        if field_options_data:
            await session.execute(insert(FieldOption), field_options_data)

        await session.commit()
        await session.refresh(form)
        return form

    @classmethod
    async def add_form(cls, data, user_id, session):
        try:
            form = Form(
                title=data.title,
                description=data.description,
                owner_id=user_id
            )
            session.add(form)
            await session.flush()

            return await cls.add_fields_and_options(data, form, session)
        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseException()

    @classmethod
    async def update_form(cls, data, form, session):
        try:
            for field in form.fields:
                await session.delete(field)

            return await cls.add_fields_and_options(data, form, session)
        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseException()
