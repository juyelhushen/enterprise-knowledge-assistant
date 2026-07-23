from pydantic import BaseModel

from app.models.citation import Citation


class WorkflowResponse(BaseModel):
    answer: str
    citations: list[Citation]