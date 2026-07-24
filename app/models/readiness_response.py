from pydantic import BaseModel


class ReadinessResponse(BaseModel):
    status: str
    chroma: bool
    ollama: bool
    embedding_model: bool
