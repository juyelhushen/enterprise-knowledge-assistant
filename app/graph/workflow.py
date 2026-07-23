from langgraph.constants import START, END
from langgraph.graph import StateGraph

from app.agents.citation_agent import CitationAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.graph.state import GraphState


def create_workflow():

    builder = StateGraph(GraphState)

    builder.add_node("retrieve", RetrievalAgent())
    builder.add_node("reason", ReasoningAgent())
    builder.add_node("cite", CitationAgent())

    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "reason")
    builder.add_edge("reason", "cite")
    builder.add_edge("cite", END)

    return builder.compile()
