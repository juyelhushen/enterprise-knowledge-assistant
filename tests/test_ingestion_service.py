from app.common.logger import get_logger

logger = get_logger(__name__)


def test_ingestion_pipeline(
    sample_pdf, ingestion_service, vector_store_repository, upload_metadata
):
    result = ingestion_service.ingest(sample_pdf, upload_metadata)

    assert result.documents_processed == 1
    assert result.chunks_created > 0

    results = vector_store_repository.similarity_search(
        "annual leave",
        k=3,
    )

    assert len(results) > 0


def test_ingestion_enriches_document_metadata(
    sample_pdf,
    upload_metadata,
    ingestion_service,
    vector_store_repository,
):
    ingestion_service.ingest(
        sample_pdf,
        upload_metadata,
    )

    stored = (
        vector_store_repository.vector_store.get(
            include=["metadatas"],
        )
    )

    metadata = stored["metadatas"][0]

    assert metadata["document_id"] == str(upload_metadata.document_id)

    assert (
        metadata["original_filename"]
        == upload_metadata.original_filename
    )

    assert (
        metadata["stored_filename"]
        == upload_metadata.stored_filename
    )

    assert (
        metadata["file_size"]
        == upload_metadata.file_size
    )

    assert "uploaded_at" in metadata
