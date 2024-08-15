from typing import Union

from pydantic import BaseModel, Field, field_validator


class CommonQueryParams(BaseModel):
    """
    Common query parameters for all endpoints

    :q: str: search query
    :page_number: int: page number
    :page_size: int: page size can't be bigger than 100
    """

    q: Union[str, None] = None
    page_number: int = Field(1, alias="page_number", gt=0)
    page_size: int = Field(25, alias="page_size", le=100)

    @field_validator("page_size", mode="before")
    def check_page_size(cls, v):
        return min(v, 100)

    @field_validator("page_number", mode="before")
    def check_page_number(cls, v):
        return max(v, 1)
