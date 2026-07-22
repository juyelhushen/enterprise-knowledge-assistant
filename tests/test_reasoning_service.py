from pathlib import Path

from app.ingestion.chunking_service import ChunkingService
from app.ingestion.document_loader import DocumentLoader
from app.services.reasoning_service import ReasoningService
from app.services.retriever_service import RetrieverService
from app.services.vector_store_service import VectorStoreService

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SAMPLE_PDF = PROJECT_ROOT / "tests" / "resources" / "sample.pdf"

def test_generate_answer():
    print("1. Creating services...")
    loader = DocumentLoader()
    chunker = ChunkingService()
    vector_store = VectorStoreService()

    vector_store.reset()


    print("2. Loading document...")
    documents = loader.load(SAMPLE_PDF)

    print("3. Chunking...")
    chunks = chunker.chunk_documents(documents)

    print("4. Adding to vector store...")
    vector_store.add_chunks(chunks)

    print("5. Retrieving...")
    retriever = RetrieverService()
    retrieved_chunks = retriever.retrieve(
        "How many annual leave days?"
    )

    print("Retrieved:", len(retrieved_chunks))

    print("6. Creating reasoning service...")
    reasoning_service = ReasoningService()

    print("7. Calling LLM...")
    prompt, answer = reasoning_service.generate_answer(
        question="How many annual leave days?",
        chunks=retrieved_chunks
    )

    print("8. Finished")

    print(answer)
