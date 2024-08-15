from typing import Dict

from fastapi import APIRouter
from app.presentation.apis.health_check.schema import HealthCheckMessage

router = APIRouter()


@router.get("/", response_model=HealthCheckMessage)
async def health_check() -> Dict[str, str]:
    """
    Health Check endpoint
    """
    return {"message": "OK"}
