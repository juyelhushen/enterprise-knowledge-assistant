from pathlib import Path

from app.common.logger import get_logger
from app.mapper.document_mapper import DocumentMapper

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SAMPLE_PDF = PROJECT_ROOT / "tests" / "resources" / "sample.pdf"

logger = get_logger(__name__)

def test_generate_answer(
    document_loader,
    chunker_service,
    vector_store_repository,
    retriever_service,
    reasoning_service,
):

    logger.info("Loading document...")
    documents = document_loader.load(SAMPLE_PDF)

    logger.info("Chunking...")
    chunks = chunker_service.chunk_documents(documents)

    docs = DocumentMapper.to_documents(chunks)

    vector_store_repository.add_documents(docs)

    logger.info("Retrieving...")
    retrieved_chunks = retriever_service.retrieve(
        "How many annual leave days?"
    )

    assert len(retrieved_chunks) > 0

    logger.info("Calling LLM...")
    prompt, answer = reasoning_service.generate_answer(
        question="How many annual leave days?",
        chunks=retrieved_chunks,
    )

    logger.info(prompt)

    assert "20" in answer
