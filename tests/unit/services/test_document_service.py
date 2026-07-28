from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.document_summary import DocumentSummary
from app.services.document_service import DocumentService


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def storage_service():
    return MagicMock()


@pytest.fixture
def document_service(repository, storage_service):
    return DocumentService(
        repository=repository,
        storage_service=storage_service,
    )


@pytest.fixture
def document_summary():
    return DocumentSummary(
        document_id="doc-123",
        original_filename="employee_handbook.pdf",
        stored_filename="3ab45cd.pdf",
        uploaded_at="2026-07-28T10:30:00Z",
        file_size=20480,
        chunks=8,
    )


def test_get_all_documents(
    document_service,
    repository,
    document_summary,
):
    repository.get_all_documents.return_value = [document_summary]

    result = document_service.get_all_documents()

    assert len(result) == 1
    assert result[0] == document_summary

    repository.get_all_documents.assert_called_once()


def test_get_document_success(
    document_service,
    repository,
    document_summary,
):
    repository.get_document.return_value = document_summary

    result = document_service.get_document("doc-123")

    assert result == document_summary

    repository.get_document.assert_called_once_with("doc-123")


def test_get_document_not_found(
    document_service,
    repository,
):
    repository.get_document.return_value = None

    with pytest.raises(HTTPException) as exc:
        document_service.get_document("invalid-id")

    assert exc.value.status_code == 404
    assert exc.value.detail == "Document not found."

    repository.get_document.assert_called_once_with("invalid-id")


def test_delete_document_success(
    document_service,
    repository,
    storage_service,
    document_summary,
):
    repository.get_document.return_value = document_summary

    document_service.delete_document("doc-123")

    repository.get_document.assert_called_once_with("doc-123")

    repository.delete_document.assert_called_once_with("doc-123")

    storage_service.delete.assert_called_once_with(
        document_summary.stored_filename
    )


def test_delete_document_not_found(
    document_service,
    repository,
    storage_service,
):
    repository.get_document.return_value = None

    with pytest.raises(HTTPException) as exc:
        document_service.delete_document("invalid-id")

    assert exc.value.status_code == 404
    assert exc.value.detail == "Document not found."

    repository.delete_document.assert_not_called()

    storage_service.delete.assert_not_called()


def test_delete_document_calls_repository_before_storage(
    document_service,
    repository,
    storage_service,
    document_summary,
):
    repository.get_document.return_value = document_summary

    document_service.delete_document("doc-123")

    repository.delete_document.assert_called_once_with("doc-123")
    storage_service.delete.assert_called_once_with(
        document_summary.stored_filename
    )