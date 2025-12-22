import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Database
    # Allow a lightweight SQLite fallback for local development when no DATABASE_URL is provided
    # If ENVIRONMENT is 'development' and DATABASE_URL env var is not set, use SQLite for convenience.
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    _default_db = (
        os.getenv("DATABASE_URL")
        or ("sqlite+aiosqlite:///./smartbank_dev.db" if ENVIRONMENT == "development" else None)
        or "postgresql+asyncpg://user:password@localhost:5432/smartbank"
    )

    DATABASE_URL: str = _default_db
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # CORS
    # Default: allow common local dev URLs for Vite/React
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,"
        "http://localhost:5173,"
        "http://127.0.0.1:3000,"
        "http://127.0.0.1:4173"
    ).split(",")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()
