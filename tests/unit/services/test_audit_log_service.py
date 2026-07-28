from datetime import datetime, timezone

import pytest

from app.models.audit_log import AuditLog


def test_log_saves_audit_record(
    audit_log_service,
    mock_repository,
):
    audit_log_service.log(
        question="What is annual leave?",
        answer="Employees receive 20 days.",
        citations=[
            {
                "source": "leave_policy.pdf",
                "page": 1,
            }
        ],
        retrieved_chunks=3,
        latency_ms=150,
    )

    mock_repository.save.assert_called_once()

    saved_log = mock_repository.save.call_args.args[0]

    assert saved_log.sources == ["leave_policy.pdf"]

    assert isinstance(saved_log, AuditLog)

    assert saved_log.question == "What is annual leave?"
    assert saved_log.answer == "Employees receive 20 days."
    assert saved_log.sources == ["leave_policy.pdf"]
    assert saved_log.retrieved_chunks == 3
    assert saved_log.latency_ms == 150
    assert saved_log.created_at is not None

def test_get_logs_returns_repository_results(
    audit_log_service,
    mock_repository,
):
    logs = [
        AuditLog(
            question="Question",
            answer="Answer",
            sources=["policy.pdf"],
            retrieved_chunks=2,
            latency_ms=120,
            created_at=datetime.now(timezone.utc),
        )
    ]
    mock_repository.find_all.return_value = logs

    result = audit_log_service.get_logs()

    assert len(result) == 1

    response = result[0]

    assert response.question == "Question"
    assert response.answer == "Answer"
    assert response.sources == ["policy.pdf"]
    assert response.retrieved_chunks == 2
    assert response.latency_ms == 120
    assert response.created_at == logs[0].created_at
    mock_repository.find_all.assert_called_once_with()


def test_clear_logs_calls_repository(
    audit_log_service,
    mock_repository,
):
    audit_log_service.clear_logs()
    mock_repository.clear.assert_called_once_with()

def test_get_logs_returns_empty_list(
    audit_log_service,
    mock_repository,
):
    mock_repository.find_all.return_value = []
    result = audit_log_service.get_logs()
    assert result == []
    mock_repository.find_all.assert_called_once_with()


def test_log_propagates_repository_exception(
    audit_log_service,
    mock_repository,
):
    mock_repository.save.side_effect = RuntimeError("Database unavailable")

    with pytest.raises(RuntimeError):
        audit_log_service.log(
            question="Question",
            answer="Answer",
            citations=[],      # ✅ new API
            retrieved_chunks=0,
            latency_ms=10,
        )