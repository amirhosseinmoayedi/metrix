from datetime import datetime

from pydantic import BaseModel


class DummyResponse(BaseModel):
    """
    DTO for dummy models.

    It returned when accessing dummy models from the API.
    """

    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class DummyRequest(BaseModel):
    """DTO for creating new dummy model."""

    name: str
