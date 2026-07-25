from langchain_chroma import Chroma

from app.core.config import settings


class ChromaFactory:

    COLLECTION_NAME = "enterprise_documents"

    @staticmethod
    def create(embedding_model) -> Chroma:

        return Chroma(
            collection_name=ChromaFactory.COLLECTION_NAME,
            embedding_function=embedding_model,
            persist_directory=settings.VECTOR_DB_PATH,
        )