import datetime

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    timestamp: datetime.datetime
    status: int
    error: str
    message: str
    path: str
