from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.settings import settings

LIMITER = Limiter(
    key_func=get_remote_address,
    # fixed-window, moving-window, fixed-window-elastic-expiry
    strategy="fixed-window-elastic-expiry",
    default_limits=[f"{settings.global_rate_limit_per_minute}/minute"],
    headers_enabled=True,
    key_prefix="limiter_",
    storage_uri=settings.rate_limit_redis_url,
)

TOO_MANY_REQUESTS_ERROR_MESSAGE = "Too many requests"


def setup_limiter(app: FastAPI):
    app.state.limiter = LIMITER
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
