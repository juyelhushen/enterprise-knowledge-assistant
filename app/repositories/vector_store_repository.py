from app.core.config import settings
from app.mapper.document_mapper import DocumentMapper
from app.models.chunk import ChunkData


class VectorStoreRepository:
    def __init__(
        self,
        vector_store
    ):
        self.vector_store = vector_store

    def add_documents(self, chunks: list[ChunkData]):
        docs = DocumentMapper.to_documents(chunks)
        self.vector_store.add_documents(docs)


    def similarity_search(
            self,
            query: str,
            k: settings.TOP_K
    ):
        return self.vector_store.similarity_search(
            query,
            k=k
        )

    def delete(
            self,
            ids: list[str]
    ):
        self.vector_store.delete(ids=ids)

    def reset(self):
        self.vector_store.delete_collection()
        # embedding_model = EmbeddingService().embedding_model
        # self.vector_store = ChromaFactory.create(embedding_model)