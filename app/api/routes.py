from fastapi import APIRouter

from app.models.ask_request import AskRequest
from app.models.workflow_response import WorkflowResponse
from app.services.workflow_service import WorkflowService
from app.models.health_response import HealthResponse
from app.services.health_service import HealthService
from app.services.readiness_service import ReadinessService
from app.models.readiness_response import ReadinessResponse

router = APIRouter()
workflow_service = WorkflowService()

health_service = HealthService()
readiness_service = ReadinessService()

@router.post(
    "/ask",
    response_model=WorkflowResponse,
)
def ask(request: AskRequest):
    return workflow_service.ask(request.question)


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