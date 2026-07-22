from typing import TypedDict
from app.models.chunk import ChunkData


class GraphState(TypedDict):
    question: str
    retrieved_chunks: list[ChunkData]

    prompt: str
    answer: str

    citations: list[dict]

