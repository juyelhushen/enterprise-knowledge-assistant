from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class AuditLog:
    question: str
    answer: str
    sources: list[str]
    retrieved_chunks: int
    latency_ms: int
    created_at: datetime