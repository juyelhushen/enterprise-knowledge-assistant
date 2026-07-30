import time

from app.common.logger import get_logger
from app.models.workflow_response import WorkflowResponse
from app.services.audit_log_service import AuditLogService

logger = get_logger(__name__)


class WorkflowService:
    """
    Facade over the LangGraph workflow.

    This service hides LangGraph from the rest of
    the application.
    """

    def __init__(
        self,
        workflow,
        audit_log_service: AuditLogService,
    ):
        self.workflow = workflow
        self.audit_log_service = audit_log_service

    def ask(
            self,
            question: str
    ) -> WorkflowResponse:

        logger.info("Workflow started")

        start = time.perf_counter()
        state = self.workflow.invoke(
            {
                "question": question,
            }
        )

        latency_ms = int((time.perf_counter() - start) * 1000)

        self.audit_log_service.log(
            question=question,
            answer=state["answer"],
            citations=state.get("citations", []),
            retrieved_chunks=len(state["retrieved_chunks"]),
            latency_ms=latency_ms,
        )

        logger.info(
            "Workflow finished in %d ms",
            latency_ms,
        )

        return WorkflowResponse(
            answer=state["answer"],
            citations=state.get("citations", [])
        )
