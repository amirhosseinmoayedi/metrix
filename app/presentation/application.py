from pathlib import Path

import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.logging import configure_logging
from app.presentation.apis.router import api_router
from app.presentation.lifespan import lifespan
from app.presentation.middlewares import add_middlewares
from app.settings import settings

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            traces_sample_rate=settings.sentry_sample_rate,
            environment=settings.environment,
            integrations=[
                FastApiIntegration(transaction_style="endpoint"),
            ],
        )

    app = FastAPI(
        title="fastapi template",
        version=settings.version,
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        lifespan=lifespan,
    )

    add_middlewares(app)

    app.include_router(router=api_router, prefix="")

    app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")

    return app
