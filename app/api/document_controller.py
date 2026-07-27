from fastapi import APIRouter, File, UploadFile

from app.dependencies.container import document_upload_service

doc_router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

@doc_router.post("")
async def upload_document(
        file: UploadFile = File(...),  # noqa: B008
):
    return await document_upload_service.upload(file)