from app.common.logger import get_logger
from app.graph.state import GraphState
from app.services.retriever_service import RetrieverService

logger = get_logger(__name__)


class RetrievalAgent:
    def __init__(self):
        self.retriever = RetrieverService()

    def __call__(self, state: GraphState) -> GraphState:
        logger.info("RetrievalAgent")

        chunks = self.retriever.retrieve(state["question"])

        state["retrieved_chunks"] = chunks

        return state
