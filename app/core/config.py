"""configuration for environment variable."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False

    # Model
    MODEL_NAME: str = "sshleifer/distilbart-cnn-12-6"
    MAX_LENGTH: int = 150
    MIN_LENGTH: int = 40

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        """Pydantic configuration class."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
