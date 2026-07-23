from fastapi import APIRouter

from app.models.ask_request import AskRequest
from app.models.workflow_response import WorkflowResponse
from app.services.workflow_service import WorkflowService

router = APIRouter()
workflow_service = WorkflowService()


@router.post(
    "/ask",
    response_model=WorkflowResponse,
)
def ask(request: AskRequest):
    return workflow_service.ask(request.question)
