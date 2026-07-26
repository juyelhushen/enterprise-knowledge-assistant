from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UploadResponse:
    filename: str
    stored_filename: str
    documents_processed: int
    chunks_created: int
    message: str