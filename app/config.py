import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_ROOT = Path(__file__).resolve().parents[1]

logger = logging.getLogger("app.config")


class Settings(BaseSettings):
    app_name: str = "Paperclip Orchestration"
    environment: str = "development"
    log_level: str = "INFO"
    database_path: Path = Path("./data/orchestration.db")

    model_config = SettingsConfigDict(
        env_file=str(APP_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def log_startup_info(self) -> None:
        logger.info("environment=%s", self.environment)
        logger.info("database_path=%s", self.database_path)


def get_settings() -> Settings:
    return Settings()
