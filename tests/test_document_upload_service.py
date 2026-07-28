import io
from pathlib import Path
from unittest.mock import ANY, Mock

import pytest
from fastapi import UploadFile

from app.models.ingestion_response import IngestionResult
from app.services.document_upload_service import DocumentUploadService


@pytest.fixture
def validator():
    return Mock()


@pytest.fixture
def storage_service():
    return Mock()


@pytest.fixture
def ingestion_service():
    return Mock()


@pytest.fixture
def upload_service(
    validator,
    storage_service,
    ingestion_service,
):
    return DocumentUploadService(
        validator=validator,
        storage_service=storage_service,
        ingestion_service=ingestion_service,
    )

def create_upload_file(
    filename: str = "employee.pdf",
    content: bytes = b"sample pdf",
) -> UploadFile:

    return UploadFile(
        filename=filename,
        file=io.BytesIO(content),
    )


@pytest.mark.asyncio
async def test_upload_document_success(
    upload_service,
    validator,
    storage_service,
    ingestion_service,
):

    upload_file = create_upload_file()

    storage_service.save.return_value = Path(
        "storage/uploaded_documents/1234.pdf"
    )

    ingestion_service.ingest.return_value = IngestionResult(
        documents_processed=1,
        chunks_created=15,
    )

    result = await upload_service.upload(upload_file)

    validator.validate.assert_called_once()

    storage_service.save.assert_called_once()

    ingestion_service.ingest.assert_called_once_with(
        Path("storage") / "uploaded_documents" / "1234.pdf",
        ANY
    )

    assert result.filename == "employee.pdf"

    assert result.stored_filename == "1234.pdf"

    assert result.documents_processed == 1

    assert result.chunks_created == 15

    assert result.message == "Document uploaded successfully."

@pytest.mark.asyncio
async def test_validation_failure_stops_processing(
    upload_service,
    validator,
    storage_service,
    ingestion_service,
):

    upload_file = create_upload_file()

    validator.validate.side_effect = ValueError("Invalid file")

    with pytest.raises(ValueError):
        await upload_service.upload(upload_file)

    storage_service.save.assert_not_called()

    ingestion_service.ingest.assert_not_called()


@pytest.mark.asyncio
async def test_storage_failure(
    upload_service,
    validator,
    storage_service,
    ingestion_service,
):

    upload_file = create_upload_file()

    storage_service.save.side_effect = OSError(
        "Disk Full"
    )

    with pytest.raises(OSError):
        await upload_service.upload(upload_file)

    validator.validate.assert_called_once()

    ingestion_service.ingest.assert_not_called()

@pytest.mark.asyncio
async def test_ingestion_failure(
    upload_service,
    validator,
    storage_service,
    ingestion_service,
):

    upload_file = create_upload_file()

    storage_service.save.return_value = Path(
        "storage/uploaded_documents/1234.pdf"
    )

    ingestion_service.ingest.side_effect = RuntimeError(
        "Embedding Failed"
    )

    with pytest.raises(RuntimeError):
        await upload_service.upload(upload_file)

    validator.validate.assert_called_once()

    storage_service.save.assert_called_once()

    ingestion_service.ingest.assert_called_once()

@pytest.mark.asyncio
async def test_file_pointer_is_reset_before_storage(
    upload_service,
    validator,
    storage_service,
    ingestion_service,
):

    upload_file = create_upload_file(
        content=b"Hello World"
    )

    storage_service.save.return_value = Path(
        "storage/uploaded_documents/1234.pdf"
    )

    ingestion_service.ingest.return_value = IngestionResult(
        documents_processed=1,
        chunks_created=5,
    )

    await upload_service.upload(upload_file)

    upload_file.file.seek(0)

    assert upload_file.file.read() == b"Hello World"