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


def test_citation_agent_removes_duplicate_citations():
    chunk1 = ChunkData(
        id="1",
        content="Leave policy",
        metadata={
            "source": "sample.pdf",
            "page": 1,
            "chunk_index": 0
        }
    )

    chunk2 = ChunkData(
        id="2",
        content="Another chunk from same page",
        metadata={
            "source": "sample.pdf",
            "page": 1,
            "chunk_index": 1
        }
    )

    state: GraphState = {
        "question": "Leave policy",
        "retrieved_chunks": [chunk1, chunk2],
        "prompt": "",
        "answer": "20 days.",
        "citations": []
    }

    agent = CitationAgent()

    result = agent(state)

    print(result["citations"])

    assert len(result["citations"]) == 1

def test_citation_agent_multiple_sources():

    chunk1 = ChunkData(
        id="1",
        content="Leave policy",
        metadata={
            "source": "employee_handbook.pdf",
            "page": 2,
            "chunk_index": 0
        }
    )

    chunk2 = ChunkData(
        id="2",
        content="Travel reimbursement",
        metadata={
            "source": "travel_policy.pdf",
            "page": 5,
            "chunk_index": 0
        }
    )

    state: GraphState = {
        "question": "Leave and travel policy",
        "retrieved_chunks": [chunk1, chunk2],
        "prompt": "",
        "answer": "...",
        "citations": []
    }

    result = CitationAgent()(state)

    assert len(result["citations"]) == 2