from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "AI Sales Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    FRONTEND_URL: str = "http://localhost:3000"
    
    # GEMINI CONFIG
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.0-flash"
    
    DUCKDB_PATH: str = str(Path(__file__).parent.parent / "data" / "sales.duckdb")
    UPLOAD_DIR: str = str(Path(__file__).parent.parent / "data" / "uploads")

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
