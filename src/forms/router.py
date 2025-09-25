from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.forms.schemas import (
    CreateOrUpdateForm,
    ResponseForm,
    ResponseFormList
)
from src.dependencies import get_current_user
from src.users.models import User
from src.forms.service import FormService


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


@router.delete('/{form_id}')
async def delete_form():
    pass


@router.post("/{form_id}/responses")
async def send_form_response():
    pass
