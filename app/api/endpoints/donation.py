from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationSuperUserDB
)
from app.services.investing import investing


router = APIRouter()


@router.get(
    '/',
    dependencies=[Depends(current_superuser)],
    response_model=list[DonationSuperUserDB],
    response_model_exclude_none=True
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Для суперюзера.

    Возвращает список всех пожертвований.
    """
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={'invested_amount'},
    response_model_exclude_none=True
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Для пользователей.

    Возвращает список пожерствований авторизованного пользователя.
    """
    donations = await donation_crud.get_by_user(session, user)
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Для зарегистрированного пользователя.

    Сделать пожертвование.
    """
    donation = await donation_crud.create(
        donation, session, user
    )
    await investing(session)
    return donation