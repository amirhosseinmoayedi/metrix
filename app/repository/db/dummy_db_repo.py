from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.db.dependencies import get_db_session
from app.repository.db.models import DummyModel


class DummyDBRepository:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):  # noqa: B008
        self.session = session

    async def all(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[DummyModel]:
        """
        method to get all the dummy object from db

        :param limit: limit the number of elements
        :param offset: skip the first n elements
        :return: list of dummy objects
        """
        raw_dummies = await self.session.execute(select(DummyModel).limit(limit).offset(offset))
        return list(raw_dummies.scalars().fetchall())

    async def get(self, identifier: int) -> DummyModel:
        """
        get a single dummy object from db

        :param identifier: pk of the object
        :return: dummy object
        """
        raw_dummy = await self.session.execute(
            select(DummyModel).filter(DummyModel.id == identifier)
        )
        return raw_dummy.scalar()

    async def create(self, name: str) -> DummyModel:
        """
        create a new dummy object in db

        :param name: name of the dummy object
        """
        new_obj = DummyModel(name=name)

        self.session.add(new_obj)
        await self.session.commit()
        await self.session.refresh(new_obj)
        return new_obj

    async def update(self, identifier: int, name: str):
        """
        update the name of the dummy object

        :param identifier: pk of the object
        :param name: new name of the object
        """
        stmt = update(DummyModel).where(DummyModel.id == identifier).values(name=name)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, identifier: int):
        """
        delete object by identifier

        :param identifier: pk of dummy object
        """
        stmt = delete(DummyModel).where(DummyModel.id == identifier)
        await self.session.execute(stmt)
        await self.session.commit()

    async def count(self) -> int:
        """
        count the number of dummy objects in the db

        :return: number of dummy objects
        """
        count = await self.session.execute(select(func.count()).select_from(DummyModel))
        return count.scalar()
