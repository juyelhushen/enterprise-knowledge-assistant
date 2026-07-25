from pathlib import Path

from app.ingestion.chunking_service import ChunkingService
from app.ingestion.document_loader import DocumentLoader
from app.prompts.prompt_builder import PromptBuilder
from app.repositories.vector_store_repository import VectorStoreRepository
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.retriever_service import RetrieverService
from app.utils.rag_debugger import RAGDebugger
from app.mapper.document_mapper import DocumentMapper

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sample_pdf = PROJECT_ROOT / "tests" / "resources" / "sample.pdf"


def main():

    loader = DocumentLoader()

    docs = loader.load(sample_pdf)

    RAGDebugger.print_documents(docs)

    chunker = ChunkingService()

    chunks = chunker.chunk_documents(docs)

    RAGDebugger.print_chunks(chunks)

    embedding = EmbeddingService()

    vector = embedding.embed_text(chunks[0].content)

    RAGDebugger.print_embedding(vector)

    store = VectorStoreRepository()

    # store.reset()


    # embedding.store_chunks(chunks)

    docs = DocumentMapper.to_documents(chunks);
    store.vector_store(docs)

    retriever = RetrieverService(store)

    retrieved = retriever.retrieve("Who won the FIFA World Cup?")

    RAGDebugger.print_retrieval(retrieved)

    builder = PromptBuilder()

    prompt = builder.build(
        "How many sick leave days?",
        retrieved,
    )

    RAGDebugger.print_prompt(prompt)

    llm = LLMService()

    response = llm.invoke(prompt)

    RAGDebugger.print_response(response.content)


if __name__ == "__main__":
    main()
