from app.common.logger import get_logger
from app.models.workflow_response import WorkflowResponse

logger = get_logger(__name__)


class WorkflowService:
    """
    Facade over the LangGraph workflow.

    This service hides LangGraph from the rest of
    the application.
    """

    def __init__(self, workflow):
        self.workflow = workflow

    def ask(self, question: str) -> WorkflowResponse:

        logger.info("Workflow started")

        state = self.workflow.invoke(
            {
                "question": question,
            }
        )

        logger.info("Workflow finished")

        return WorkflowResponse(
            answer=state["answer"],
            citations=state["citations"],
        )
