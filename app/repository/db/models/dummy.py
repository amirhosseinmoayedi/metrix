from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from app.repository.db.base import Base


class DummyModel(Base):
    """Model for demo purpose."""

    __tablename__ = "dummy_model"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=200))

    class Config:
        orm_mode = True

    def __repr__(self):
        return f"<DummyModel(id={self.id}, name={self.name})>"

    def __str__(self):
        return f"<DummyModel(id={self.id}, name={self.name})>"
