from app.ingestion.chunking_service import ChunkingService
from app.models.document import DocumentData
import uuid


def test_chunk_documents_returns_chunks():
    # Arrange
    service = ChunkingService()

    document = DocumentData(
        content=(
            "Employee Handbook. " * 100
        ),
        metadata={
            "source": "sample.pdf",
            "page": 1,
        },
    )

    # Act
    chunks = service.chunk_documents([document])

    # Assert
    assert len(chunks) > 0

def test_chunk_metadata_is_preserved():
    service = ChunkingService()

    document = DocumentData(
        content="Hello World " * 100,
        metadata={
            "source": "sample.pdf",
            "page": 5,
        },
    )

    chunks = service.chunk_documents([document])

    for chunk in chunks:
        assert chunk.metadata["source"] == "sample.pdf"
        assert chunk.metadata["page"] == 5


def test_chunk_index_is_added():
    service = ChunkingService()

    document = DocumentData(
        content="Hello World " * 200,
        metadata={},
    )

    chunks = service.chunk_documents([document])

    for index, chunk in enumerate(chunks):
        assert chunk.metadata["chunk_index"] == index



def test_chunk_has_valid_uuid():
    service = ChunkingService()

    document = DocumentData(
        content="Python " * 200,
        metadata={},
    )

    chunks = service.chunk_documents([document])

    for chunk in chunks:
        uuid.UUID(chunk.id)


def test_empty_document_returns_no_chunks():
    service = ChunkingService()

    document = DocumentData(
        content="",
        metadata={},
    )

    chunks = service.chunk_documents([document])

    assert chunks == []