from app.graph.state import GraphState
from common.logger import get_logger

logger = get_logger(__name__)

class CitationAgent:
    """
    Responsible for extracting citations from the
    retrieved chunks
    """

    def __call__(self, state: GraphState) -> GraphState:

        logger.info("CitationAgent")

        seen = set()
        citations = []

        for chunk in state["retrieved_chunks"]:
            citation = (
                chunk.metadata.get("source"),
                chunk.metadata.get("page"),
            )

            if citation not in seen:
                seen.add(citation)

                citations.append(
                    {
                        "source": citation[0],
                        "page": citation[1],
                    }
                )

        state["citations"] = citations

        return state
