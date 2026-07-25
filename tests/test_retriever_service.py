from app.common.logger import get_logger

logger = get_logger(__name__)


def test_retrieve_policy(
    sample_pdf,
    ingestion_service,
    retriever_service,
):
    ingestion_service.ingest(str(sample_pdf))

    chunks = retriever_service.retrieve("How many annual leave days do employees receive?")

    print("length-------------", len(chunks))

    for chunk in chunks:
        print("chunk ::::::::::::", chunk)

    assert len(chunks) > 0
    assert "20 days" in chunks[0].content
