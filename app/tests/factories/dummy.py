import factory
from sqlalchemy import delete

from app.repository.db.models.dummy import DummyModel
from app.tests.factories.session import get_session


class DummyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DummyModel
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("name")

    @classmethod
    def clean_up(cls):
        stmnt = delete(DummyModel).where()
        cls._meta.sqlalchemy_session.execute(stmnt)
        cls._meta.sqlalchemy_session.commit()
