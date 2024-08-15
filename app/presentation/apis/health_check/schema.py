from pydantic import BaseModel


class HealthCheckMessage(BaseModel):

    message: str
