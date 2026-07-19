from pathlib import Path

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

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()