"""
Application configuration using Pydantic settings
Loads from environment variables and .env file
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Basic settings
    APP_NAME: str = "H.O.M.E. Platform"
    DEBUG: bool = False
    VERSION: str = "0.1.0"
    
    # API settings
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.run.app",
    ]
    
    # GCP Settings
    GCP_PROJECT_ID: str
    GCP_REGION: str = "us-central1"
    FIRESTORE_DATABASE: str = "(default)"
    
    # Firebase Auth
    FIREBASE_PROJECT_ID: str = ""
    
    # Twilio (SMS)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # SendGrid (Email)
    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = ""
    
    # Redis (optional for Phase 0)
    REDIS_URL: str = ""
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )


# Global settings instance
settings = Settings()
