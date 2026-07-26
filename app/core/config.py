from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    OLLAMA_BASE_URL: str
    LLM_MODEL: str
    EMBEDDING_MODEL: str
    VECTOR_DB_PATH: str

    TOP_K: int
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int

    UPLOAD_DIRECTORY: str = "storage/uploaded_documents"

    MAX_UPLOAD_SIZE_MB: int = 10

    ALLOWED_EXTENSIONS: list[str] = Field(
        default_factory=lambda: [
            "pdf",
            "docx",
            "txt",
        ]
    )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", case_sensitive=True, extra="ignore"
    )


settings = Settings()
