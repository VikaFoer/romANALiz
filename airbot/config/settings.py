"""Pydantic settings from .env – all secrets and config in one place."""
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated app settings from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/airbot.db",
        alias="DATABASE_URL",
    )
    kafka_bootstrap_servers: str = Field(default="localhost:9092", alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic: str = Field(default="airbot.events", alias="KAFKA_TOPIC")
    kafka_enabled: bool = Field(default=False, alias="KAFKA_ENABLED")
    webhook_url: str = Field(default="", alias="WEBHOOK_URL")
    webhook_enabled: bool = Field(default=False, alias="WEBHOOK_ENABLED")
    soc_mint_enabled: bool = Field(default=False, alias="SOC_MINT_ENABLED")
    nlp_model_path: str = Field(default="", alias="NLP_MODEL_PATH")
    worker_pool_size: int = Field(default=4, ge=1, le=64, alias="WORKER_POOL_SIZE")
    queue_max_size: int = Field(default=10_000, ge=1, le=1_000_000, alias="QUEUE_MAX_SIZE")
    port: int = Field(default=8000, ge=1, le=65535, alias="PORT")


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
