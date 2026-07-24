
from app.common.logger import get_logger
from app.ingestion.ingestion_service import IngestionService
from app.services.rag_service import RAGService
from app.services.vector_store_service import VectorStoreService

logger = get_logger(__name__)


def test_rag_answers_question(sample_pdf):
    store = VectorStoreService()

    try:
        store.reset()
    except RuntimeError as e:
        logger.warning("Vector store reset failed: %s", e)

    ingestion = IngestionService()

    ingestion.ingest(str(sample_pdf))

    rag = RAGService()

    answer = rag.answer("How many annual leave days do employees receive?")

    assert isinstance(answer, str)

    assert "20" in answer
