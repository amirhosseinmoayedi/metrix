import enum
import tomllib
from pathlib import Path
from tempfile import gettempdir
from typing import Set, Optional
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    """log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Environments(str, enum.Enum):
    """different environments that code runs on"""

    DEV = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: Optional[str] = "127.0.0.1"
    port: Optional[int] = 8000

    workers_count: Optional[int] = 1  # quantity of workers for uvicorn
    reload: Optional[bool] = False  # Enable uvicorn reloading

    environment: Optional[str] = Environments.PRODUCTION  # Current environment

    log_level: Optional[LogLevel] = LogLevel.WARNING

    allowed_hosts: Optional[Set[str]] = {"*"}

    gzip_min_size: Optional[int] = 1000

    allow_origins: Optional[Set[str]] = {"*"}
    allow_methods: Optional[Set[str]] = {"*"}
    allow_headers: Optional[Set[str]] = {"*"}
    allow_credentials: Optional[bool] = False

    sentry_dsn: Optional[str] = None
    sentry_sample_rate: Optional[float] = 1.0

    # This variable is used to define
    # multiproc_dir. It's required for [uvi|guni]corn projects.
    prometheus_dir: Optional[Path] = TEMP_DIR / "prom"

    postgres_dsn: PostgresDsn
    test_db_name: str = "test_db"

    enable_global_rate_limit: bool = False
    global_rate_limit_per_minute: int = 1000
    rate_limit_redis_url: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        env_file_encoding="utf-8",
    )

    @property
    def version(self) -> str:
        with open("pyproject.toml", "rb") as f:
            toml_data = tomllib.load(f)
        # Attempt to get the version from different possible locations
        version: str = toml_data.get("tool", {}).get("poetry", {}).get("version")
        return version

    @property
    def test_db_url(self) -> str:
        return str(self.postgres_dsn).replace(
            settings.postgres_dsn.path, f"/{settings.test_db_name}"
        )


settings = Settings()
