from app.ingestion.chunking_service import ChunkingService
from app.ingestion.document_loader import DocumentLoader
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

    def ingest(self, file_path: str):

        documents = self.loader.load(file_path)

        chunks = self.chunker.chunk_documents(documents)

        self.repository.add_documents(chunks)

        return {
            "documents": len(documents),
            "chunks": len(chunks),
        }
