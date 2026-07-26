from pydantic.dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class IngestionResult:
    documents_processed: int
    chunks_created: int