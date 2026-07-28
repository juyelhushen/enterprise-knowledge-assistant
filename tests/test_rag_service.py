from app.common.logger import get_logger

logger = get_logger(__name__)


def test_rag_answers_question(
    sample_pdf, ingestion_service, rag_service, upload_metadata
):
    ingestion_service.ingest(sample_pdf, upload_metadata)

    answer = rag_service.answer("How many annual leave days do employees receive?")

    assert isinstance(answer, str)
    assert "20" in answer
