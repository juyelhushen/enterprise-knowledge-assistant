from app.ingestion.ingestion_service import IngestionService
from app.services.rag_service import RAGService
from app.services.vector_store_service import VectorStoreService


def test_rag_answers_question(sample_pdf):
    store = VectorStoreService()

    try:
        store.reset()
    except Exception:
        pass

    ingestion = IngestionService()

    ingestion.ingest(str(sample_pdf))

    rag = RAGService()

    answer = rag.answer(
        "How many annual leave days do employees receive?"
    )

    assert isinstance(answer, str)

    assert "20" in answer