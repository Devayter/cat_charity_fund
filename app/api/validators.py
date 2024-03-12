from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


CHARITY_PROJECT_NOT_FOUND = 'Благотворительный проект не найден'
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
    charity_project_id: int,
    session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project.fully_invested is True:
        raise HTTPException(
            detail=PROJECT_HAS_ALREADY_CLOSED,
            status_code=HTTPStatus.BAD_REQUEST
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if not charity_project:
        raise HTTPException(
            detail=CHARITY_PROJECT_NOT_FOUND,
            status_code=HTTPStatus.NOT_FOUND
        )
    return charity_project


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession
) -> None:
    charity_project_id = (
        await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
    ).scalars().first()
    if charity_project_id:
        raise HTTPException(
            detail=NAME_ALREADY_EXIST,
            status_code=HTTPStatus.BAD_REQUEST
        )


async def check_new_full_amount(
    charity_project_full_amount: int,
    charity_project_id: int,
    session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project_full_amount < charity_project.invested_amount:
        raise HTTPException(
            detail=NEW_FULL_AMOUNT_ERROR,
            status_code=HTTPStatus.BAD_REQUEST
        )
    if charity_project_full_amount == charity_project.invested_amount:
        charity_project.fully_invested = True


def check_invested_before_delete(
    charity_project: CharityProject
) -> None:
    if charity_project.invested_amount > 0:
        raise HTTPException(
            detail=UNABLE_TO_DELETE,
            status_code=HTTPStatus.BAD_REQUEST
        )
