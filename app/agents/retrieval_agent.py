from app.graph.state import GraphState
from app.services.retriever_service import RetrieverService


class RetrievalAgent:
    def __init__(self):
        self.retriever = RetrieverService()

    def __call__(self, state: GraphState) -> GraphState:
        print("RetrievalAgent")

        chunks = self.retriever.retrieve(state["question"])

        state["retrieved_chunks"] = chunks

        return state
