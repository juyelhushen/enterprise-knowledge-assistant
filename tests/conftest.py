import logging
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from langchain_ollama import OllamaEmbeddings

from app.agents.citation_agent import CitationAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.core.config import settings
from app.dependencies.container import get_audit_log_repository
from app.dto.upload_metadata import UploadMetadata
from app.graph.workflow import create_workflow
from app.infrastructure.chroma_factory import ChromaFactory
from app.ingestion.chunking_service import ChunkingService
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.ingestion_service import IngestionService
from app.main import app
from app.prompts.prompt_builder import PromptBuilder
from app.repositories.vector_store_repository import VectorStoreRepository
from app.services.audit_log_service import AuditLogService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.services.reasoning_service import ReasoningService
from app.services.retriever_service import RetrieverService
from app.services.workflow_service import WorkflowService

logger = logging.getLogger(__name__)


@pytest.fixture
def embedding_model():
    return OllamaEmbeddings(
        model=settings.EMBEDDING_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
    )


@pytest.fixture(scope="session")
def sample_pdf():
    return Path("tests/resources/sample.pdf")


@pytest.fixture(scope="session")
def document_loader():
    return DocumentLoader()


@pytest.fixture(scope="session")
def chunker_service():
    return ChunkingService()


@pytest.fixture(scope="session")
def embedding_service():
    return EmbeddingService()


@pytest.fixture
def vector_store(embedding_model):
    return ChromaFactory.create(embedding_model)


@pytest.fixture
def retrieval_agent(retriever_service):
    return RetrievalAgent(
        retriever_service,
    )


# @pytest.fixture
# def vector_store_repository(vector_store):
#     return VectorStoreRepository(vector_store)


@pytest.fixture
def vector_store_repository(vector_store):
    repository = VectorStoreRepository(vector_store)

    # Clean before every test
    repository.reset()

    yield repository

    # Clean after every test
    repository.reset()


@pytest.fixture
def ingestion_service(
    document_loader,
    chunker_service,
    vector_store_repository,
):
    return IngestionService(
        loader=document_loader,
        chunker=chunker_service,
        repository=vector_store_repository,
    )


@pytest.fixture
def retriever_service(vector_store_repository):
    return RetrieverService(vector_store_repository)


@pytest.fixture
def prompt_builder():
    return PromptBuilder()


@pytest.fixture
def llm_service():
    return LLMService()


@pytest.fixture
def rag_service(
    retriever_service,
    prompt_builder,
    llm_service,
):
    return RAGService(
        retriever=retriever_service,
        prompt_builder=prompt_builder,
        llm_service=llm_service,
    )


@pytest.fixture
def reasoning_service(prompt_builder, llm_service):
    return ReasoningService(
        prompt_builder=prompt_builder,
        llm_service=llm_service,
    )


@pytest.fixture
def reasoning_agent(reasoning_service):
    return ReasoningAgent(reasoning_service)


@pytest.fixture
def citation_agent():
    return CitationAgent()


@pytest.fixture
def seeded_vector_store(
    ingestion_service,
    sample_pdf,
    upload_metadata,
):
    ingestion_service.ingest(
        sample_pdf,
        upload_metadata,
    )


@pytest.fixture
def workflow(retrieval_agent, reasoning_agent, citation_agent, seeded_vector_store):
    return create_workflow(
        retrieval_agent,
        reasoning_agent,
        citation_agent,
    )


@pytest.fixture
def workflow_service(workflow):
    return WorkflowService(
        workflow
    )


@pytest.fixture
def upload_metadata():

    return UploadMetadata(
        document_id=uuid4(),
        original_filename="sample.pdf",
        stored_filename="a1b2c3d4.pdf",
        uploaded_at=datetime.now(timezone.utc),
        file_size=1024,
    )


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


# audit
@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def audit_log_service(mock_repository):
    return AuditLogService(
        repository=mock_repository,
    )


@pytest.fixture(autouse=True)
def clean_audit_logs():
    repository = get_audit_log_repository()
    repository.clear()

    yield

    repository.clear()


@pytest.fixture(autouse=True)
def clean_test_data(vector_store_repository):
    get_audit_log_repository().clear()
    vector_store_repository.reset()

    yield

    get_audit_log_repository().clear()
    vector_store_repository.reset()