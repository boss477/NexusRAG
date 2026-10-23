from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NexusRAG"
    environment: str = Field(default="development", pattern="^(development|test|staging|production)$")
    log_level: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    api_prefix: str = "/api/v1"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    redis_url: str = "redis://localhost:6379/0"
    langchain_tracing_v2: bool = False
    langchain_api_key: str | None = None
    langchain_project: str = "NexusRAG"
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    embedding_provider: str = "hash-test"
    gemini_embedding_model: str = "gemini-embedding-2"
    embedding_dimension: int = 1536
    tavily_api_key: str | None = None

    @field_validator("api_prefix")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        if not value.startswith("/"):
            raise ValueError("api_prefix must start with '/'")
        return value.rstrip("/") or "/"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

