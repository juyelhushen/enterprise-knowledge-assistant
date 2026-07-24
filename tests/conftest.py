import logging
from pathlib import Path

import pytest

from app.ingestion.chunking_service import ChunkingService
from app.ingestion.document_loader import DocumentLoader
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def sample_pdf():
    return Path("tests/resources/sample.pdf")


@pytest.fixture(scope="session")
def loader():
    return DocumentLoader()


@pytest.fixture(scope="session")
def chunker():
    return ChunkingService()


@pytest.fixture(scope="session")
def embedding_service():
    return EmbeddingService()


@pytest.fixture()
def vector_store():
    store = VectorStoreService()

    # Clean database before each test
    try:
        store.reset()
    except RuntimeError as e:
        logger.warning("Vector store reset failed: %s", e)

    return VectorStoreService()
