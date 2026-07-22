from app.agents.citation_agent import CitationAgent
from app.graph.state import GraphState
from app.models.chunk import ChunkData


def test_citation_agent():
    chunk = ChunkData(
        id="chunk-1",
        content="Employees receive 20 days of paid annual leave.",
        metadata={
            "source": "sample.pdf",
            "page": 1,
            "chunk_index": 0
        }
    )

    state: GraphState = {
        "question": "How many annual leave days?",
        "retrieved_chunks": [chunk],
        "prompt": "",
        "answer": "20 days.",
        "citations": []
    }

    agent = CitationAgent()

    result = agent(state)

    print(result["citations"])

    assert len(result["citations"]) == 1
    assert result["citations"][0]["source"] == "sample.pdf"
    assert result["citations"][0]["page"] == 1
