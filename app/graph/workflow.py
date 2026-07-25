from langgraph.graph import END, START, StateGraph

from app.agents.citation_agent import CitationAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.graph.state import GraphState


def create_workflow(
    retrieval_agent: RetrievalAgent,
    reasoning_agent: ReasoningAgent,
    citation_agent: CitationAgent,
):
    builder = StateGraph(GraphState)

    builder.add_node("retrieve", retrieval_agent)
    builder.add_node("reason", reasoning_agent)
    builder.add_node("cite", citation_agent)

    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "reason")
    builder.add_edge("reason", "cite")
    builder.add_edge("cite", END)

    return builder.compile()