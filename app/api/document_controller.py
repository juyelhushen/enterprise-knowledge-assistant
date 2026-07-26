from fastapi import APIRouter, File, UploadFile

from app.dependencies.container import document_upload_service

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

@router.post("")
async def upload_document(
        file: UploadFile = File(...),  # noqa: B008
):
    return await document_upload_service.upload(file)