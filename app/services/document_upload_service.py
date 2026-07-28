from datetime import datetime, timezone
from uuid import uuid4

from fastapi import UploadFile

from app.dto.upload_metadata import UploadMetadata
from app.ingestion.ingestion_service import IngestionService
from app.models.upload_response import UploadResponse
from app.services.file_storage_service import FileStorageService
from app.validators.file_validator import FileValidator


class DocumentUploadService:

    def __init__(
            self,
            validator: FileValidator,
            storage_service: FileStorageService,
            ingestion_service: IngestionService,
    ):
        self.validator = validator
        self.storage_service = storage_service
        self.ingestion_service = ingestion_service

    async def upload(
            self,
            file: UploadFile
    ) -> UploadResponse:

        contents = await file.read()

        self.validator.validate(
            filename=file.filename,
            size=len(contents),
        )

        file.file.seek(0)

        stored_path = self.storage_service.save(file)

        metadata = UploadMetadata(
            document_id=uuid4(),
            original_filename=file.filename,
            stored_filename=stored_path.name,
            uploaded_at=datetime.now(timezone.utc),
            file_size=len(contents),
        )

        ingestion_result = self.ingestion_service.ingest(
            stored_path,
            metadata
        )

        return UploadResponse(
            filename=file.filename,
            stored_filename=stored_path.name,
            documents_processed=ingestion_result.documents_processed,
            chunks_created=ingestion_result.chunks_created,
            message="Document uploaded successfully.",
        )

