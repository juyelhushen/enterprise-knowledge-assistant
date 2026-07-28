from typing import Annotated

from fastapi import APIRouter, Depends, File, Response, UploadFile, status

from app.dependencies.container import (
    document_upload_service,
    get_document_service,
)
from app.models.document_summary import DocumentSummary
from app.services.document_service import DocumentService

doc_router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@doc_router.post("")
async def upload_document(
        file: UploadFile = File(...),  # noqa: B008
):
    return await document_upload_service.upload(file)



@doc_router.get(
    "",
    response_model=list[DocumentSummary],
    status_code=status.HTTP_200_OK,
)
def get_documents(
    service: Annotated[
        DocumentService,
        Depends(get_document_service),
    ],
):
    return service.get_all_documents()


@doc_router.get(
    "/{document_id}",
    response_model=DocumentSummary,
    status_code=status.HTTP_200_OK,
)
def get_document(
    document_id: str,
    service: Annotated[
        DocumentService,
        Depends(get_document_service),
    ],
):
    return service.get_document(document_id)


@doc_router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    document_id: str,
    service: Annotated[
        DocumentService,
        Depends(get_document_service),
    ],
):
    service.delete_document(document_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )