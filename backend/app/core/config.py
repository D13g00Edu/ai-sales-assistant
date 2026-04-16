from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
class Settings(BaseSettings):
    APP_NAME: str = 'AI Sales Assistant Modular'; DEBUG: bool = True; FRONTEND_URL: str = 'http://localhost:3000'
    GEMINI_API_KEY: str = ''; GEMINI_MODEL: str = 'gemini-1.5-flash'
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_RAW_DIR: str = str(BASE_DIR / 'data' / 'raw')
    DATA_PROCESSED_DIR: str = str(BASE_DIR / 'data' / 'processed')
    DUCKDB_PATH: str = str(BASE_DIR / 'data' / 'db' / 'sales.duckdb')
    class Config: env_file = '.env'; case_sensitive = True; extra = 'ignore'; extra = "ignore"
@lru_cache()
def get_settings(): return Settings()