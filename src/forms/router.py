from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.forms.schemas import (
    CreateOrUpdateForm,
    ResponseForm,
    ResponseFormList,
    CreateAnswer
)
from src.dependencies import get_current_user
from src.users.models import User
from src.forms.service import FormService, FormResponseService


router = APIRouter(
    prefix='/api/v1/forms',
    tags=['Forms']
)


@router.post('/')
async def create_form(
    data: CreateOrUpdateForm,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> dict:
    form = await FormService.create_form(data, user.id, session)
    return {
            "message": "Form created successfully",
            "form_id": form.id
        }


@router.get('/{form_id}')
async def get_form(
    form_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> ResponseForm:
    form = await FormService.get_forms(form_id, session)
    return ResponseForm.model_validate(form)


@router.get('/')
async def get_my_form(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    forms = await FormService.get_my_forms(user.id, session)
    return ResponseFormList(forms=forms)


@router.patch('/{form_id}')
async def update_form(
    form_id: int,
    update_data: CreateOrUpdateForm,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> ResponseForm:
    return await FormService.update_form(form_id, update_data, session)


@router.delete('/{form_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_form(
    form_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    await FormService.delete_form(form_id, user.id, session)


@router.post("/{form_id}/responses")
async def send_form_response(
    form_id: int,
    response_data: CreateAnswer,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    response_id = await FormResponseService.submit_response(
            form_id=form_id,
            user_id=user.id,
            answers=response_data.answers,
            session=session
        )

    return {
        "message": "Response submitted successfully",
        "response_id": response_id,
        "form_id": form_id
    }
