from app.models.chunk import ChunkData
from app.repositories.vector_store_repository import VectorStoreRepository


class RetrieverService:

    def __init__(
            self,
            repository: VectorStoreRepository
    ):
        self.repository = repository

    def retrieve(
        self,
        question: str,
        top_k: int = 3,
    ) -> list[ChunkData]:
        documents = self.repository.similarity_search(question, k=top_k)

        chunks = []

        for doc in documents:
            chunks.append(
                ChunkData(
                    id=doc.id,
                    content=doc.page_content,
                    metadata=doc.metadata,
                )
            )
        return chunks
