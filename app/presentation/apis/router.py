"""
Main router for the API.
"""

from fastapi import APIRouter

from app.presentation.apis import health_check
from app.presentation.apis.v1 import router as api_router_v1

api_router = APIRouter()


api_router.include_router(health_check.router, prefix="/health", tags=["health_check"])
api_router.include_router(api_router_v1, prefix="/api/v1")
