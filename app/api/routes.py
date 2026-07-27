from fastapi import APIRouter

from app.dependencies.container import workflow_service
from app.models.ask_request import AskRequest
from app.models.health_response import HealthResponse
from app.models.readiness_response import ReadinessResponse
from app.models.workflow_response import WorkflowResponse
from app.services.health_service import HealthService
from app.services.readiness_service import ReadinessService

router = APIRouter()
workflow = workflow_service

health_service = HealthService()
readiness_service = ReadinessService()

@router.post(
    "/ask",
    response_model=WorkflowResponse,
)
def ask(request: AskRequest):
    return workflow.ask(request.question)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns whether the application is alive.",
)
def health():
    return health_service.health()


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    summary="Readiness Check",
    description="Check whether the application is ready to serve requests.",
)
def ready():
    return readiness_service.ready()