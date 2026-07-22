from attr import dataclass

from app.models.citation import Citation


@dataclass(slots=True)
class WorkflowResponse:
    answer: str
    citations: list[Citation]