from app.infrastructure.chroma_factory import ChromaFactory
from app.repositories.vector_store_repository import VectorStoreRepository
from app.services.embedding_service import EmbeddingService
from app.services.retriever_service import RetrieverService

embedding_service=EmbeddingService()

vector_store=ChromaFactory.create(
    embedding_service.embedding_model
)

vector_store_repository=VectorStoreRepository(
    vector_store
)

retriever_service= RetrieverService(
    vector_store_repository
)
