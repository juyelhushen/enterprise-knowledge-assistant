from fastapi import APIRouter

from app.models.ask_request import AskRequest
from app.services.workflow_service import WorkflowService
router = APIRouter()

workflow_service = WorkflowService()

@router.post("/ask")
def ask(request: AskRequest):

    print("Received request")

    response = workflow_service.ask(request.question)

    print("Returning response")

    return response
