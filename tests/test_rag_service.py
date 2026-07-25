
from app.common.logger import get_logger

logger = get_logger(__name__)


def test_rag_answers_question(
    sample_pdf,
    ingestion_service,
    rag_service,
):
    ingestion_service.ingest(str(sample_pdf))

    answer = rag_service.answer(
        "How many annual leave days do employees receive?"
    )

    assert isinstance(answer, str)
    assert "20" in answer
