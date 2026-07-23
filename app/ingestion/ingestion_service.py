from app.ingestion.chunking_service import ChunkingService
from app.ingestion.document_loader import DocumentLoader
from app.services.vector_store_service import VectorStoreService


class IngestionService:
    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = ChunkingService()
        self.vector_store = VectorStoreService()

    def ingest(self, file_path: str):
        documents = self.loader.load(file_path)
        chunks = self.chunker.chunk_documents(documents)
        self.vector_store.add_chunks(chunks)

        return {
            "documents": len(documents),
            "chunks": len(chunks),
        }
