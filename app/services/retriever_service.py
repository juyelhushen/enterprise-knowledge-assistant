from app.models.chunk import ChunkData
from app.services.vector_store_service import VectorStoreService


class RetrieverService:
    def __init__(self):
        self.vector_store = VectorStoreService()

    def retrieve(
        self,
        question: str,
        top_k: int | None = None,
    ) -> list[ChunkData]:
        results = self.vector_store.similarity_search(question, k=top_k)

        chunks = []

        for doc in results:
            chunks.append(
                ChunkData(
                    id=doc.id,
                    content=doc.page_content,
                    metadata=doc.metadata,
                )
            )
        return chunks
