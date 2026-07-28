from app.dto.audit_log_response import AuditLogResponse
from app.models.audit_log import AuditLog


class AuditLogMapper:

    @staticmethod
    def to_response(
        audit_log: AuditLog,
    ) -> AuditLogResponse:

        return AuditLogResponse(
            question=audit_log.question,
            answer=audit_log.answer,
            sources=audit_log.sources,
            retrieved_chunks=audit_log.retrieved_chunks,
            latency_ms=audit_log.latency_ms,
            created_at=audit_log.created_at,
        )