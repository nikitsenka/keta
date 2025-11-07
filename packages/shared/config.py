"""
Configuration management for KETA.
"""

from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProvider(str, Enum):
    LOCAL = "local"
    AZURE = "azure"
    OPENAI = "openai"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "KETA"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/keta_db"
    db_pool_min_size: int = 5
    db_pool_max_size: int = 20

    # Graph
    graph_name: str = "keta_graph"

    # LLM Configuration
    llm_provider: LLMProvider = LLMProvider.LOCAL
    model_temperature: float = 0.0
    model_max_retries: int = 5
    model_timeout: int = 120

    # Azure Mistral (production)
    azure_mistral_endpoint: Optional[str] = None
    azure_mistral_api_key: Optional[str] = None
    mistral_model: str = "mistral-large-latest"

    # Local Ollama (development)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral"

    # OpenAI (optional fallback)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.0

    # Extraction
    max_chunk_size: int = 10000  # characters
    extraction_timeout: int = 300  # seconds

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings instance
    """
    return Settings()
