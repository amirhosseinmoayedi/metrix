from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.presentation.limiter import setup_limiter
from app.presentation.utils import setup_prometheus
from app.repository.db.utils import setup_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    on start up behaviour is before the yield and shutdown is after the yield

    :param app:
    """
    # startup
    print("started")
    app.middleware_stack = None
    setup_prometheus(app)
    setup_limiter(app)

    await setup_db(app)
    app.middleware_stack = app.build_middleware_stack()
    yield
    # shutdown
    await close_db(app)
