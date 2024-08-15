from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from loguru import logger
from starlette import status
from starlette.requests import Request

from app.presentation.apis.v1.dummy.schema import DummyResponse, DummyRequest
from app.presentation.limiter import LIMITER, TOO_MANY_REQUESTS_ERROR_MESSAGE
from app.presentation.dependecies import CommonQueryParams
from app.repository.db.models import DummyModel
from app.service import DummyService

router = APIRouter(tags=["dummy"])


@cbv(router)
class DummyView:

    def __init__(self, service: DummyService = Depends(DummyService)):  # noqa: B008
        self.service: DummyService = service

    @router.get(
        "/error",
        response_description="server sample error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        responses={
            status.HTTP_429_TOO_MANY_REQUESTS: {"description": TOO_MANY_REQUESTS_ERROR_MESSAGE}
        },
    )
    @LIMITER.limit("1/minute", error_message=TOO_MANY_REQUESTS_ERROR_MESSAGE)
    async def get_dummy_error(self, request: Request):
        """
        for testing logging.

        :raise value error and log it with logger, then raise http exception with status code 500.
        """
        try:
            raise ValueError("Dummy error")
        except ValueError as e:
            logger.bind(type="DUMMY").error("Dummy error")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e

    @router.get("/", status_code=status.HTTP_200_OK, response_model=List[DummyResponse])
    async def get_dummies(
        self, commons_params: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
    ) -> list[DummyModel]:
        """
        Retrieve all dummy objects from the database.

        :param q: search query.
        :param skip: number of items to skip.
        :param limit: number of items to return.
        :return: list of dummy objects from database.
        """
        return await self.service.get_all()

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=DummyResponse)
    async def create_dummy_model(self, dummy_object: DummyRequest) -> DummyModel:
        """
        Creates dummy model in the database.

        :param dummy_object: new dummy model item.
        """
        return await self.service.create(dummy_object.name)

    @router.get("/{dummy_id}", status_code=status.HTTP_200_OK, response_model=DummyResponse)
    async def get_dummy_model(self, dummy_id: int) -> DummyModel:
        """
        Retrieve a dummy object from the database.

        :param dummy_id: id of the dummy object.
        :return: dummy object from a database.
        """
        return await self.service.get(dummy_id)

    @router.patch("/{dummy_id}", status_code=status.HTTP_200_OK)
    async def update_dummy_model(self, dummy_id: int, dummy_object: DummyRequest) -> None:
        """
        Updates a dummy object in the database.

        :param dummy_id: id of the dummy object.
        :param dummy_object: updated dummy object.
        """
        await self.service.update(dummy_id, dummy_object.name)

    @router.delete("/{dummy_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_dummy_model(self, dummy_id: int) -> None:
        """
        Deletes a dummy object from the database.

        :param dummy_id: id of the dummy object.
        """
        await self.service.delete(dummy_id)
