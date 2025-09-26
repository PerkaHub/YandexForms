from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[M]:
    model: type[M]

    @classmethod
    async def get_one_or_none(
        cls, session: AsyncSession, **filter_by
    ) -> M | None:
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(
        cls, session, **filter_by
    ) -> list[M]:
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add_data(cls, session, **data):
        try:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
        except Exception:
            await session.rollback()

    @classmethod
    async def delete_data(cls, session, **data):
        query = delete(cls.model).filter_by(**data)
        await session.execute(query)
        await session.commit()
