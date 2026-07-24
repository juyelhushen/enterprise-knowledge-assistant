from langchain_ollama import OllamaEmbeddings

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.embedding_model = OllamaEmbeddings(
            model=settings.EMBEDDING_MODEL, base_url=settings.OLLAMA_BASE_URL
        )

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text.
        """
        return self.embedding_model.embed_query(text)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """
        return self.embedding_model.embed_documents(texts)
