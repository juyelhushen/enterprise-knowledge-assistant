from app.ingestion.ingestion_service import IngestionService
from app.services.retriever_service import RetrieverService
from app.services.vector_store_service import VectorStoreService


def test_retrieve_policy(sample_pdf):
    store = VectorStoreService()

    try:
        store.reset()
    except Exception:
        pass

    store = VectorStoreService()
    ingesttion = IngestionService()

    ingesttion.ingest(str(sample_pdf))

    retriever = RetrieverService()

    chunks = retriever.retrieve("How many annual leave days do employees receive?")

    print("length-------------", len(chunks))

    for chunk in chunks:
        print("chunk ::::::::::::", chunk)

    assert len(chunks) > 0
    assert "20 days" in chunks[0].content
