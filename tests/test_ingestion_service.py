
from app.common.logger import get_logger

logger = get_logger(__name__)

def test_ingestion_pipeline(
    sample_pdf,
    ingestion_service,
    vector_store_repository,
):
    result = ingestion_service.ingest(str(sample_pdf))

    assert result["documents"] == 1
    assert result["chunks"] > 0

    results = vector_store_repository.similarity_search(
        "annual leave",
        k=3,
    )

    assert len(results) > 0
