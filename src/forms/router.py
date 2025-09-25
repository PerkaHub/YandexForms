from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix='/api/v1/forms',
    tags=['Forms']
)


@router.post('/')
async def create_form():
    pass


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
