from pathlib import Path

from app.agents.citation_agent import CitationAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.graph.workflow import create_workflow
from app.infrastructure.chroma_factory import ChromaFactory
from app.infrastructure.persistence.sqlite.sqlite_audit_log_repository import (
    SQLiteAuditLogRepository,
)
from app.ingestion.chunking_service import ChunkingService
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.ingestion_service import IngestionService
from app.prompts.prompt_builder import PromptBuilder
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.vector_store_repository import VectorStoreRepository
from app.services.audit_log_service import AuditLogService
from app.services.document_service import DocumentService
from app.services.document_upload_service import DocumentUploadService
from app.services.embedding_service import EmbeddingService
from app.services.file_storage_service import FileStorageService
from app.services.llm_service import LLMService
from app.services.reasoning_service import ReasoningService
from app.services.retriever_service import RetrieverService
from app.services.workflow_service import WorkflowService
from app.validators.file_validator import FileValidator

# Infrastructure
embedding_service = EmbeddingService()

vector_store = ChromaFactory.create(embedding_service.embedding_model)

# Repository
vector_store_repository = VectorStoreRepository(vector_store)

# Domain Services
document_loader = DocumentLoader()

chunking_service = ChunkingService()

retriever_service = RetrieverService(vector_store_repository)

ingestion_service = IngestionService(
    loader=document_loader,
    chunker=chunking_service,
    repository=vector_store_repository,
)

# Upload Services
document_validator = FileValidator()

file_storage_service = FileStorageService()

document_upload_service = DocumentUploadService(
    validator=document_validator,
    storage_service=file_storage_service,
    ingestion_service=ingestion_service,
)

document_service = DocumentService(vector_store_repository, file_storage_service)


def get_document_service() -> DocumentService:
    return document_service


prompt_builder = PromptBuilder()

llm_service = LLMService()

retrieval_agent = RetrievalAgent(retriever_service)

reasoning_service = ReasoningService(prompt_builder, llm_service)

reasoning_agent = ReasoningAgent(reasoning_service)

citation_agent = CitationAgent()

workflow = create_workflow(
    retrieval_agent=retrieval_agent,
    reasoning_agent=reasoning_agent,
    citation_agent=citation_agent,
)

# audit
_audit_log_repository: AuditLogRepository | None = None
_audit_log_service: AuditLogService | None = None


def get_audit_log_repository() -> AuditLogRepository:
    global _audit_log_repository

    if _audit_log_repository is None:
        _audit_log_repository = SQLiteAuditLogRepository(
            database_path=Path("data/audit_logs.db"),
        )

    return _audit_log_repository


def get_audit_log_service() -> AuditLogService:
    global _audit_log_service

    if _audit_log_service is None:
        _audit_log_service = AuditLogService(
            repository=get_audit_log_repository(),
        )

    return _audit_log_service


audit_log_service = get_audit_log_service()
workflow_service = WorkflowService(
    workflow=workflow, audit_log_service=get_audit_log_service()
)
