from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DocumentSummary:
    document_id: str
    original_filename: str
    stored_filename: str
    uploaded_at: str
    file_size: int
    chunks: int