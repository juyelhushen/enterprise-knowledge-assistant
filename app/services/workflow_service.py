from app.graph.workflow import create_workflow
from app.models.workflow_response import WorkflowResponse


class WorkflowService:
    """
    Facade over the LangGraph workflow.

    This service hides LangGraph from the rest of
    the application.
    """

    def __init__(self):
        self.workflow = create_workflow()

    def ask(self, question: str) -> WorkflowResponse:
        state = self.workflow.invoke(
            {
                "question": question,
            }
        )

        return WorkflowResponse(
            answer=state["answer"],
            citations=state["citations"],
        )

