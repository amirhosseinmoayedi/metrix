from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.settings import settings


async def setup_db(app: FastAPI):
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """

    engine = create_async_engine(str(settings.postgres_dsn), echo=True)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


async def close_db(app: FastAPI):
    """
    Closes the database connection.

    :param app: fastAPI application.
    """
    await app.state.db_engine.dispose()
