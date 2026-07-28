from collections import defaultdict

from app.core.config import settings
from app.mapper.document_mapper import DocumentMapper
from app.models.chunk import ChunkData
from app.models.document_summary import DocumentSummary


class VectorStoreRepository:
    def __init__(
        self,
        vector_store
    ):
        self.vector_store = vector_store

    def add_documents(self, chunks: list[ChunkData]):
        docs = DocumentMapper.to_documents(chunks)
        self.vector_store.add_documents(docs)

    def get_all_metadata(self) -> list[dict]:
        response = self.vector_store.get(include=["metadatas"])
        return response["metadatas"]


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
        result = self.vector_store.get()
        ids = result.get("ids", [])

        if len(ids) > 0:
            self.vector_store.delete(ids=ids)

    # def reset(self):
        # self.vector_store.delete_collection()
        # self.vector_store.delete(ids=self.vector_store.get()["ids"])

        # self.vector_store = ChromaFactory.create(self.vector_store._embedding_function)

    def get_all_documents(self) -> list[DocumentSummary]:

        response = self.vector_store.get(include=["metadatas"])

        grouped = defaultdict(list)

        for metadata in response["metadatas"]:
            grouped[metadata["document_id"]].append(metadata)

        documents = []

        for document_id, chunks in grouped.items():
            first = chunks[0]

            documents.append(
                DocumentSummary(
                    document_id=document_id,
                    original_filename=first["original_filename"],
                    stored_filename=first["stored_filename"],
                    uploaded_at=first["uploaded_at"],
                    file_size=first["file_size"],
                    chunks=len(chunks),
                )
            )

        return sorted(
            documents,
            key=lambda d: d.uploaded_at,
            reverse=True,
        )


    def get_document(
        self,
        document_id: str,
    ) -> DocumentSummary | None:

        documents = self.get_all_documents()

        for document in documents:
            if document.document_id == document_id:
                return document

        return None


    def delete_document(
        self,
        document_id: str,
    ):

        response = self.vector_store.get(include=[], where={"document_id": document_id})

        ids = response["ids"]

        if ids:
            self.vector_store.delete(ids=ids)