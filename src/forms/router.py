from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.forms.schemas import CreateForm
from src.dependencies import get_current_user
from src.users.models import User
from src.forms.service import FormService


router = APIRouter(
    prefix='/api/v1/forms',
    tags=['Forms']
)


@router.post('/')
async def create_form(
    data: CreateForm,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    try:
        form = await FormService.create_form(data, user.id, session)
        return {
                "message": "Form created successfully",
                "form_id": form.id
            }
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error creating form: {str(e)}"
        )


@router.get('/{form_id}')
async def get_form():
    pass


@router.get('/')
async def get_my_form():
    pass


@router.patch('/{form_id}')
async def update_form():
    pass


@router.delete('/{form_id}')
async def delete_form():
    pass


@router.post("/{form_id}/responses")
async def send_form_response():
    pass
