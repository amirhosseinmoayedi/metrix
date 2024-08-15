from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from slowapi.middleware import SlowAPIMiddleware

from app.settings import settings, Environments


def add_middlewares(app: FastAPI):
    """
    Add middlewares to the FastAPI application.

    :param app:
    """

    if settings.environment is Environments.PRODUCTION:
        app.add_middleware(HTTPSRedirectMiddleware)

    if settings.enable_global_rate_limit:
        app.add_middleware(SlowAPIMiddleware)

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)

    app.add_middleware(GZipMiddleware, minimum_size=settings.gzip_min_size)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_methods=settings.allow_methods,
        allow_headers=settings.allow_headers,
        allow_credentials=settings.allow_credentials,
    )
