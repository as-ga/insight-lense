import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings from environment variables."""

    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # Environment
    ENVIRONMENT: str = os.getenv("FLASK_ENV", "development")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # CORS
    CORS_ORIGIN: str = os.getenv("CORS_ORIGIN", "http://localhost:5173")

    class Config:
        env_file = ".env"


settings = Settings()
