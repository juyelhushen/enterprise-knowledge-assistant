from langchain_core.documents import Document
from langchain_chroma import Chroma

from app.core.config import settings
from app.models.chunk import ChunkData
from app.services.embedding_service import EmbeddingService


class VectorStoreService:
    COLLECTION_NAME = "enterprise_documents"

    def __init__(self):
        self.embedding_service = EmbeddingService()

        self.vector_store = Chroma(
            collection_name=self.COLLECTION_NAME,
            embedding_function=self.embedding_service.embedding_model,
            persist_directory=settings.VECTOR_DB_PATH
        )

    def add_documents(self, documents):
        """
        Store LangChain Document objects in ChromaDB.
        """
        self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int | None = None):
        """
        Search for the most relevant documents.
        """
        return self.vector_store.similarity_search(query, k=k or settings.TOP_K)

    def reset(self):
        """
        Delete the current collection.
        """
        self.vector_store.delete_collection();

    def add_chunks(self, chunks: list[ChunkData]):
        documents = []

        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk.content,
                    metadata=chunk.metadata,
                    id=chunk.id,
                )
            )

        self.vector_store.add_documents(documents)