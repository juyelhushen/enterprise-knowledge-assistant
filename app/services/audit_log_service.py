from datetime import datetime, timezone

from app.mapper.audit_log_mapper import AuditLogMapper
from app.models.audit_log import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository


class AuditLogService:

    def __init__(
        self,
        repository: AuditLogRepository,
    ):
        self.repository = repository

    def log(
        self,
        question: str,
        answer: str,
        citations: list[dict],
        retrieved_chunks: int,
        latency_ms: int,
    ) -> None:

        sources = [
            citation["source"]
            for citation in citations
        ]

        audit_log = AuditLog(
            question=question,
            answer=answer,
            sources=sources,
            retrieved_chunks=retrieved_chunks,
            latency_ms=latency_ms,
            created_at=datetime.now(timezone.utc),
        )

        self.repository.save(audit_log)

    def get_logs(self):

        logs = self.repository.find_all()

        return [AuditLogMapper.to_response(log) for log in logs]

    def clear_logs(self) -> None:
        self.repository.clear()

