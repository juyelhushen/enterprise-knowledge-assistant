from app.ingestion.ingestion_service import IngestionService
from app.services.vector_store_service import VectorStoreService


def test_ingestion_pipeline(sample_pdf):
    store = VectorStoreService()

    try:
        store.reset()
    except Exception:
        pass
    store = VectorStoreService()
    service = IngestionService()
    result = service.ingest(str(sample_pdf))

    assert result["documents"] == 1
    assert result["chunks"] > 0

    results = store.similarity_search("annual leave")

    assert len(results) > 0
