from fastapi import HTTPException, status

from app.repositories.vector_store_repository import VectorStoreRepository
from app.services.file_storage_service import FileStorageService


class DocumentService:

    def __init__(
            self,
            repository: VectorStoreRepository,
            storage_service: FileStorageService
    ):
        self.repository = repository
        self.storage_service = storage_service

    def get_all_documents(self):
        return self.repository.get_all_documents()


    def get_document(self, document_id: str):
        document = self.repository.get_document(document_id)

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found."
            )

        return document


    def delete_document(self, document_id: str):
        document = self.repository.get_document(document_id)

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found."
            )

        self.repository.delete_document(document_id)
        self.storage_service.delete(
            document.stored_filename
        )

