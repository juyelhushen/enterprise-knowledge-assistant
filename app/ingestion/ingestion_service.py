from pathlib import Path

from app.dto.upload_metadata import UploadMetadata
from app.ingestion.chunking_service import ChunkingService
from app.ingestion.document_loader import DocumentLoader
from app.models.ingestion_response import IngestionResult
from app.repositories.vector_store_repository import VectorStoreRepository


class IngestionService:

    def __init__(
        self,
        loader: DocumentLoader,
        chunker: ChunkingService,
        repository: VectorStoreRepository
    ):
        self.loader = loader
        self.chunker = chunker
        self.repository = repository

    def ingest(
            self,
            file_path: Path,
            upload_metadata: UploadMetadata
    ) -> IngestionResult:

        documents = self.loader.load(file_path)

        for document in documents:
            document.metadata["document_id"] = str(upload_metadata.document_id)
            document.metadata["original_filename"] = upload_metadata.original_filename
            document.metadata["stored_filename"] = upload_metadata.stored_filename
            document.metadata["uploaded_at"] = upload_metadata.uploaded_at.isoformat()
            document.metadata["file_size"] = upload_metadata.file_size

        chunks = self.chunker.chunk_documents(documents)

        self.repository.add_documents(chunks)

        return IngestionResult(
            documents_processed=len(documents),
            chunks_created=len(chunks)
        )
