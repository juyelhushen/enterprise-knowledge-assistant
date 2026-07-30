from langgraph.graph import END, START, StateGraph

from app.agents.citation_agent import CitationAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.core.constants import NO_ANSWER_FOUND
from app.graph.state import GraphState


def should_generate_citations(state: GraphState):
    """
    Decide whether the CitationAgent should execute.

    If the LLM could not answer the question from the retrieved
    context, skip citation generation and finish the workflow.
    """
    if state["answer"].strip() == NO_ANSWER_FOUND:
        return END

    return "cite"


def create_workflow(
    retrieval_agent: RetrievalAgent,
    reasoning_agent: ReasoningAgent,
    citation_agent: CitationAgent,
):
    builder = StateGraph(GraphState)

    # Nodes
    builder.add_node("retrieve", retrieval_agent)
    builder.add_node("reason", reasoning_agent)
    builder.add_node("cite", citation_agent)

    # Flow
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "reason")

    # Conditionally execute CitationAgent
    builder.add_conditional_edges(
        "reason",
        should_generate_citations,
        {
            "cite": "cite",
            END: END,
        },
    )

    builder.add_edge("cite", END)

    return builder.compile()