from app.common.logger import get_logger
from app.graph.state import GraphState
from app.prompts.prompt_builder import PromptBuilder
from app.services.reasoning_service import ReasoningService

logger = get_logger(__name__)

class ReasoningAgent:

    def __init__(
        self,
        reasoning_service: ReasoningService,
    ):
        self.reasoning_service = reasoning_service

    def __call__(self, state: GraphState) -> GraphState:
        logger.info("ReasoningAgent")

        prompt, answer = self.reasoning_service.generate_answer(
            question=state["question"],
            chunks=state["retrieved_chunks"],
        )

        state["prompt"] = prompt
        state["answer"] = answer

        return state
