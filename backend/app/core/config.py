"""
Configuration management for H.O.M.E. Platform
Uses pydantic-settings to load from environment variables
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    """Application settings loaded from environment"""
    
    # Application
    env: str = "development"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # GCP
    gcp_project_id: str
    gcp_region: str = "us-central1"
    
    # Firestore
    firestore_database: str = "(default)"
    
    # Cloud SQL (optional for Phase 0)
    cloudsql_connection_name: str = ""
    db_user: str = "postgres"
    db_pass: str = ""
    db_name: str = "home_platform"
    
    # Vertex AI (Phase 1+)
    vertex_ai_location: str = "us-central1"
    vertex_ai_model: str = "claude-3-sonnet@20240229"
    
    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""
    
    # SendGrid
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = ""
    sendgrid_from_name: str = "H.O.M.E. Platform"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    
    # Security
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: str = "http://localhost:3000"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    # Demo
    demo_mode: bool = True
    demo_qr_codes: int = 5
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

# Create global settings instance
settings = Settings()
