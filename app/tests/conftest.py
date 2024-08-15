from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import make_url, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from starlette.testclient import TestClient

from app.presentation.application import get_app
from app.repository.db.dependencies import get_db_session
from app.settings import settings


async def create_database():
    """Create a database."""
    db_url = make_url(str(settings.test_db_url.replace(settings.test_db_name, "")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
    db_name = settings.test_db_name
    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                f"SELECT 1 FROM pg_database WHERE datname='{db_name}'",  # noqa: E501, S608
            )
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        await drop_database()

    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(
            text(
                f'CREATE DATABASE "{db_name}" ENCODING "utf8" TEMPLATE template1',  # noqa: E501
            )
        )


async def drop_database():
    """Drop current database."""
    db_url = make_url(str(settings.test_db_url.replace(settings.test_db_name, "")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
    db_name = settings.test_db_name
    async with engine.connect() as conn:
        disc_users = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
            "FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{db_name}' "
            "AND pid <> pg_backend_pid();"
        )
        await conn.execute(text(disc_users))
        await conn.execute(text(f'DROP DATABASE "{db_name}"'))


def load_all_models() -> None:
    """Load all models from this folder."""
    from app.repository.db.models import DummyModel  # noqa: F401


@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from app.repository.db.base import META  # noqa: WPS433

    load_all_models()

    await create_database()

    engine = create_async_engine(settings.test_db_url)
    async with engine.begin() as conn:
        await conn.run_sync(META.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
def client(dbsession: AsyncSession) -> TestClient:
    """
    Fixture that creates client for requesting server.

    :param dbsession:
    :yield: client for the app.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    return TestClient(app=application)


@pytest.fixture
async def async_client(dbsession: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """ """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    async with AsyncClient(app=application, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"
