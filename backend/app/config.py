"""Application settings loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    content_dir: str = str(Path(__file__).resolve().parents[2] / "content")
    rate_limit: str = "30/minute"
    max_request_size_bytes: int = 65_536

    sandbox_image: str = "codecraft-sandbox:latest"
    sandbox_timeout_seconds: int = 5
    sandbox_memory_mb: int = 256
    sandbox_pids_limit: int = 64
    sandbox_output_limit_bytes: int = 65_536
    sandbox_network: str = "none"
    sandbox_disabled: bool = False

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def content_path(self) -> Path:
        return Path(self.content_dir)


@lru_cache
def get_settings() -> Settings:
    return Settings()
