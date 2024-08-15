from fastapi import Depends

from app.repository.db.dummy_db_repo import DummyDBRepository
from app.repository.db.models import DummyModel


class DummyService:
    def __init__(
        self, db_repository: DummyDBRepository = Depends(DummyDBRepository)  # noqa: B008
    ):
        self.db_repository = db_repository

    async def get_all(self) -> list[DummyModel]:
        """
        get all dummy models from the database

        :return: list of dummy models
        """
        dummies = await self.db_repository.all()
        return dummies

    async def get(self, identifier: int) -> DummyModel:
        """
        get dummy model by identifier

        :param identifier: pk of the dummy model
        :return: dummy model
        """
        return await self.db_repository.get(identifier)

    async def create(self, name: str) -> DummyModel:
        """
        create a new dummy model

        :param name:
        """
        return await self.db_repository.create(name)

    async def update(self, identifier: int, name: str):
        await self.db_repository.update(identifier, name)

    async def delete(self, identifier: int):
        await self.db_repository.delete(identifier)
