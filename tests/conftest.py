import logging
import pytest

from langchain_ollama import OllamaEmbeddings
from pathlib import Path

from app.agents.citation_agent import CitationAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.core.config import settings
from app.infrastructure.chroma_factory import ChromaFactory
from app.ingestion.chunking_service import ChunkingService
from app.ingestion.ingestion_service import IngestionService
from app.services.embedding_service import EmbeddingService
from app.services.rag_service import RAGService
from app.services.retriever_service import RetrieverService
from app.services.llm_service import LLMService
from app.repositories.vector_store_repository import VectorStoreRepository
from app.prompts.prompt_builder import PromptBuilder
from app.ingestion.document_loader import DocumentLoader
from app.graph.workflow import create_workflow

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
def chunker():
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
#     repository = VectorStoreRepository(vector_store)
#     repository.reset()
#
#     yield repository

    # repository.reset()

@pytest.fixture
def vector_store_repository(vector_store):
    return VectorStoreRepository(vector_store)

@pytest.fixture
def ingestion_service(
    document_loader,
    chunker,
    vector_store_repository,
):
    return IngestionService(
        loader=document_loader,
        chunker=chunker,
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
def reasoning_agent():
    return ReasoningAgent()


@pytest.fixture
def citation_agent():
    return CitationAgent()

@pytest.fixture
def workflow(
    retrieval_agent,
    reasoning_agent,
    citation_agent,
):
    return create_workflow(
        retrieval_agent,
        reasoning_agent,
        citation_agent,
    )