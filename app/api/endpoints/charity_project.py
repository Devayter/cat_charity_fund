from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists, check_fully_invested_status,
    check_invested_before_delete, check_name_duplicate, check_new_full_amount
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.investing import investing


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Доступно для всех.

    Вернуть список всех благотворительных проектов.
    """
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    response_model_exclude_unset=True
)
async def create_charity_project(
    obj_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Для суперюзера.

    Создать новый благотворительный проект.
    """
    await check_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.create(
        obj_in, session, need_commit=False
    )
    session.add_all(
        investing(charity_project, await donation_crud.get_opened(session))
    )
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.patch(
    '/{project_id}',
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Для суперюзера.

    Изменить название, описание проекта. Установить новую сумму (не должна быть
    меньше внесенной). Нельзя редактировать закрытые проекты.
    """
    charity_project = await check_charity_project_exists(
        project_id,
        session
    )
    await check_fully_invested_status(project_id, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_new_full_amount(
            obj_in.full_amount, project_id, session
        )
    charity_project = await charity_project_crud.update(
        charity_project,
        obj_in,
        session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Для суперюзера.

    Удалить выбранный проект. Нельзя удалить закрытый проект или проект, в
    который уже были инвестированы средства.
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    check_invested_before_delete(charity_project)
    return await charity_project_crud.remove(charity_project, session)
