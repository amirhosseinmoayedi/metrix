import sqlalchemy
from sqlalchemy.orm import DeclarativeBase

META = sqlalchemy.MetaData()


class Base(DeclarativeBase):
    """Base for all models."""

    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()
    )

    metadata = META
