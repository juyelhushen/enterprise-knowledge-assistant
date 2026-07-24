
from app.common.logger import get_logger
from app.ingestion.ingestion_service import IngestionService
from app.services.vector_store_service import VectorStoreService

logger = get_logger(__name__)

def test_ingestion_pipeline(sample_pdf):
    store = VectorStoreService()

    try:
        store.reset()
    except RuntimeError as e:
        logger.warning("Vector store reset failed: %s", e)

    store = VectorStoreService()
    service = IngestionService()
    result = service.ingest(str(sample_pdf))

    assert result["documents"] == 1
    assert result["chunks"] > 0

    results = store.similarity_search("annual leave")

    assert len(results) > 0
