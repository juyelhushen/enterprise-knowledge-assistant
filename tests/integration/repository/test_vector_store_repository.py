def test_get_all_documents_returns_uploaded_document(
    sample_pdf,
    upload_metadata,
    ingestion_service,
    vector_store_repository,
):
    ingestion_service.ingest(
        sample_pdf,
        upload_metadata,
    )

    documents = vector_store_repository.get_all_documents()

    assert len(documents) == 1

    document = documents[0]

    assert document.document_id == str(upload_metadata.document_id)
    assert document.original_filename == upload_metadata.original_filename
    assert document.stored_filename == upload_metadata.stored_filename
    assert document.file_size == upload_metadata.file_size
    assert document.chunks > 0

def test_get_document_returns_document(
    sample_pdf,
    upload_metadata,
    ingestion_service,
    vector_store_repository,
):
    ingestion_service.ingest(
        sample_pdf,
        upload_metadata,
    )

    document = vector_store_repository.get_document(
        str(upload_metadata.document_id)
    )

    assert document is not None
    assert document.document_id == str(upload_metadata.document_id)
    assert document.original_filename == upload_metadata.original_filename
    assert document.stored_filename == upload_metadata.stored_filename
    assert document.file_size == upload_metadata.file_size
    assert document.chunks > 0

from uuid import uuid4


def test_get_document_returns_none_for_unknown_document(
    vector_store_repository,
):
    document = vector_store_repository.get_document(
        str(uuid4())
    )

    assert document is None

def test_delete_document_removes_all_chunks(
    sample_pdf,
    upload_metadata,
    ingestion_service,
    vector_store_repository,
):
    ingestion_service.ingest(
        sample_pdf,
        upload_metadata,
    )

    assert (
        vector_store_repository.get_document(
            str(upload_metadata.document_id)
        )
        is not None
    )

    vector_store_repository.delete_document(
        str(upload_metadata.document_id)
    )

    assert (
        vector_store_repository.get_document(
            str(upload_metadata.document_id)
        )
        is None
    )

def test_similarity_search_returns_empty_after_document_deleted(
    sample_pdf,
    upload_metadata,
    ingestion_service,
    vector_store_repository,
):
    ingestion_service.ingest(
        sample_pdf,
        upload_metadata,
    )

    vector_store_repository.delete_document(
        str(upload_metadata.document_id)
    )

    results = vector_store_repository.similarity_search(
        "annual leave",
        k=3,
    )

    assert len(results) == 0