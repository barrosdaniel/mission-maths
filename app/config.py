"""Application configuration.

Reads settings from environment variables and an optional .env file.
Never hard-code secrets — use environment variables or a vault.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All application settings, resolved from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/mission_maths"
    db_echo: bool = False

    # Application
    app_env: str = "development"
    secret_key: str = "change-me-in-production"
    debug: bool = False


settings = Settings()
