from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.crud.charity_project import charityproject_crud


CHARITYPROJECT_NOT_FOUND = 'Благотворительный проект не найден'
UNABLE_TO_DELETE = (
    'Невозможно удалить проект, в который уже были инвестированы средства, '
    'его можно только закрыть'
)
NEW_FULL_AMOUNT_ERROR = (
    'Новая сумма пожертвований не может быть меньше вложенной'
)
NAME_ALREADY_EXIST = 'Такое имя уже существует'
PROJECT_HAS_ALREADY_CLOSED = 'Данный проект уже закрыт'


async def check_fully_invested_status(
        charityproject_id: int,
        session: AsyncSession
) -> None:
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if charityproject.fully_invested is True:
        raise HTTPException(
            detail=PROJECT_HAS_ALREADY_CLOSED,
            status_code=HTTPStatus.BAD_REQUEST
        )


async def check_charityproject_exists(
        charityproject_id: int,
        session: AsyncSession
) -> CharityProject:
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if not charityproject:
        raise HTTPException(
            detail=CHARITYPROJECT_NOT_FOUND,
            status_code=HTTPStatus.NOT_FOUND
        )
    return charityproject


async def check_name_duplicate(
    charityproject_name: str,
    session: AsyncSession
) -> None:
    charityproject_id = await session.execute(
        select(CharityProject.id).where(
            CharityProject.name == charityproject_name
        )
    )
    charityproject_id = charityproject_id.scalars().first()
    if charityproject_id:
        raise HTTPException(
            detail=NAME_ALREADY_EXIST,
            status_code=HTTPStatus.BAD_REQUEST
        )


async def check_new_full_amount(
        charityproject_full_amount: int,
        charityproject_id: int,
        session: AsyncSession
) -> None:
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if charityproject_full_amount < charityproject.invested_amount:
        raise HTTPException(
            detail=NEW_FULL_AMOUNT_ERROR,
            status_code=HTTPStatus.BAD_REQUEST
        )
    if charityproject_full_amount == charityproject.invested_amount:
        charityproject.fully_invested = True


async def check_invested_before_delete(
        charityproject: CharityProject,
        session: AsyncSession
) -> None:
    if charityproject.invested_amount > 0:
        raise HTTPException(
            detail=UNABLE_TO_DELETE,
            status_code=HTTPStatus.BAD_REQUEST
        )
