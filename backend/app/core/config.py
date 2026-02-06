from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "RankForge AI"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # AI Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    SERPER_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # Database
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
