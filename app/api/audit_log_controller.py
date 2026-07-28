from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.dependencies.container import get_audit_log_service
from app.dto.audit_log_response import AuditLogResponse
from app.services.audit_log_service import AuditLogService

audit_router = APIRouter(
    prefix="/logs",
    tags=["Audit Logs"],
)


@audit_router.get(
    "",
    response_model=list[AuditLogResponse],
)
def get_logs(
    service: Annotated[
        AuditLogService,
        Depends(get_audit_log_service),
    ],
):

    return service.get_logs()



@audit_router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
def clear_logs(
    service: Annotated[
        AuditLogService,
        Depends(get_audit_log_service),
    ],
):

    service.clear_logs()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )

