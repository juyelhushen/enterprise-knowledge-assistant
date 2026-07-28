from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True, frozen=True)
class UploadMetadata:
    document_id: UUID
    original_filename: str
    stored_filename: str
    uploaded_at: datetime
    file_size: int