from app.graph.state import GraphState
from app.services.reasoning_service import ReasoningService


class ReasoningAgent:

    def __init__(self):
        self.reasoning_service = ReasoningService()


    def __call__(self, state: GraphState) -> GraphState:

        prompt, answer = self.reasoning_service.generate_answer(
            question=state["question"],
            chunks=state["retrieved_chunks"],
        )

        state["prompt"] = prompt
        state["answer"] = answer

        return state