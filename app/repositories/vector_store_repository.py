from langchain_core.documents import Document

from app.core.config import settings


class VectorStoreRepository:
    def __init__(
        self,
        vector_store
    ):
        self.vector_store = vector_store

    def add_documents(self, documents: list[Document]):
        self.vector_store.add_documents(documents)


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