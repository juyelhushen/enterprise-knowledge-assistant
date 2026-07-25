from pathlib import Path

from langchain_ollama import OllamaEmbeddings

from app.core.config import settings
from app.infrastructure.chroma_factory import ChromaFactory
from app.ingestion.chunking_service import ChunkingService
from app.ingestion.document_loader import DocumentLoader
from app.mapper.document_mapper import DocumentMapper
from app.prompts.prompt_builder import PromptBuilder
from app.repositories.vector_store_repository import VectorStoreRepository
from app.services.llm_service import LLMService
from app.services.retriever_service import RetrieverService
from app.utils.rag_debugger import RAGDebugger

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sample_pdf = PROJECT_ROOT / "tests" / "resources" / "sample.pdf"


def main():
    # Infrastructure
    loader = DocumentLoader()
    chunker = ChunkingService()

    embedding_model = OllamaEmbeddings(
        model=settings.EMBEDDING_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
    )

    vector_store = ChromaFactory.create(embedding_model)
    repository = VectorStoreRepository(vector_store)

    # Services
    # embedding_service = EmbeddingService()
    retriever = RetrieverService(repository)
    prompt_builder = PromptBuilder()
    llm = LLMService()

    # Load & Chunk
    docs = loader.load(sample_pdf)
    RAGDebugger.print_documents(docs)

    chunks = chunker.chunk_documents(docs)
    RAGDebugger.print_chunks(chunks)

    # Store
    mappedDocs = DocumentMapper.to_documents(chunks)
    repository.add_documents(mappedDocs)

    # Retrieve
    retrieved = retriever.retrieve(
        "Who won the FIFA World Cup?",
        settings.TOP_K,
    )
    RAGDebugger.print_retrieval(retrieved)

    # Prompt
    prompt = prompt_builder.build(
        "How many sick leave days?",
        retrieved,
    )
    RAGDebugger.print_prompt(prompt)

    # LLM
    response = llm.invoke(prompt)
    RAGDebugger.print_response(response)


if __name__ == "__main__":
    main()
