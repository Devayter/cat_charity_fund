from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

FORBIDDEN_FIELDS = (
    'invested_amount', 'fully_invested', 'create_date', 'close_date'
)
EDIT_FIELD_ERROR = 'Поле {field} запрещено для редактирования.'


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
        need_commit: bool = True
    ):
        obj_in_data = obj_in.model_dump()
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if need_commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ):
        return (await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )).scalars().first()

    async def get_opened(
        self,
        session: AsyncSession
    ):
        return (await session.execute(
            select(self.model).where(
                not_(self.model.fully_invested)
            )
        )).scalars().all()

    async def get_multi(
        self,
        session: AsyncSession
    ):
        return (await session.execute(select(self.model))).scalars().all()

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            if field in FORBIDDEN_FIELDS:
                raise HTTPException(
                    detail=EDIT_FIELD_ERROR.format(field=field),
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY
                )
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
