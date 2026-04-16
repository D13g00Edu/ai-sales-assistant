import os

def write_file(path, content):
    full_path = os.path.join(r"c:\Users\diego\Desktop\proyectos\Mlops", path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created/Updated: {path}")

# ======================= SCHEMAS =======================
write_file("backend/app/schemas/requests.py", '''
from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str
    dataset_id: str = "default_sales"
''')

write_file("backend/app/schemas/responses.py", '''
from typing import Any
from pydantic import BaseModel

class UploadPipelineResponse(BaseModel):
    dataset_id: str
    status: str
    rows_processed: int
    message: str

class AnalyticsSummaryResponse(BaseModel):
    total_sales: float
    total_transactions: int
    avg_ticket: float
    unique_products: int
    unique_clients: int

class AnalyticsTrendResponse(BaseModel):
    mes: str
    total: float

class AnalyticsRankingResponse(BaseModel):
    nombre: str
    total: float

class AskResponse(BaseModel):
    question: str
    sql_executed: str
    data: list[dict[str, Any]]
    human_summary: str

class ForecastItem(BaseModel):
    ds: str
    yhat: float
    yhat_lower: float
    yhat_upper: float

class ForecastResponse(BaseModel):
    historical: list[dict[str, Any]]
    forecast: list[ForecastItem]
''')

# ======================= CORE =======================
write_file("backend/app/core/config.py", '''
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "AI Sales Assistant Modular"
    DEBUG: bool = True
    FRONTEND_URL: str = "http://localhost:3000"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Rutas absolutas a los Data Layers
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_RAW_DIR: str = str(BASE_DIR / "data" / "raw")
    DATA_PROCESSED_DIR: str = str(BASE_DIR / "data" / "processed")
    DUCKDB_PATH: str = str(BASE_DIR / "data" / "db" / "application.duckdb")

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
''')

write_file("backend/app/core/exceptions.py", '''
class ValidationError(Exception):
    def __init__(self, message: str, errors: list = None):
        super().__init__(message)
        self.errors = errors or []

class SecurityError(Exception):
    pass
''')

write_file("backend/app/core/security.py", '''
def is_safe_sql_query(sql_query: str) -> bool:
    q = sql_query.upper().strip()
    return q.startswith("SELECT") and not any(
        kw in q for kw in ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "ALTER"]
    )
''')

# ======================= INFRASTRUCTURE =======================
write_file("backend/app/infrastructure/database.py", '''
import duckdb
from pathlib import Path
from app.core.config import get_settings

_conn: duckdb.DuckDBPyConnection | None = None

class DuckDBRepository:
    def __init__(self):
        settings = get_settings()
        Path(settings.DUCKDB_PATH).parent.mkdir(parents=True, exist_ok=True)
        global _conn
        if _conn is None:
            _conn = duckdb.connect(database=settings.DUCKDB_PATH, read_only=False)
        self.conn = _conn

    def execute_query(self, query: str):
        return self.conn.execute(query).df()

    def load_parquet_to_view(self, view_name: str, parquet_path: str):
        # En DuckDB, conviene mapear parquet directo en lugar de insert si es inmutable
        query = f"CREATE OR REPLACE VIEW {view_name} AS SELECT * FROM read_parquet('{parquet_path}')"
        self.conn.execute(query)
''')

write_file("backend/app/infrastructure/storage.py", '''
import os
import shutil
from app.core.config import get_settings

class LocalFileStorage:
    def __init__(self):
        self.settings = get_settings()
        os.makedirs(self.settings.DATA_RAW_DIR, exist_ok=True)
        os.makedirs(self.settings.DATA_PROCESSED_DIR, exist_ok=True)

    def save_raw_stream(self, dataset_id: str, file_stream) -> str:
        filepath = os.path.join(self.settings.DATA_RAW_DIR, f"{dataset_id}.xlsx")
        with open(filepath, "wb") as f:
            shutil.copyfileobj(file_stream, f)
        return filepath

    def get_processed_filepath(self, dataset_id: str) -> str:
        return os.path.join(self.settings.DATA_PROCESSED_DIR, f"{dataset_id}.parquet")
''')

write_file("backend/app/infrastructure/llm_client.py", '''
import google.generativeai as genai
from app.core.config import get_settings
from app.core.exceptions import SecurityError

class GeminiClient:
    def __init__(self):
        self.settings = get_settings()
        if self.settings.GEMINI_API_KEY:
            genai.configure(api_key=self.settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.settings.GEMINI_MODEL)

    def prompt(self, instructions: str) -> str:
        if not self.settings.GEMINI_API_KEY:
            raise SecurityError("GEMINI API Key not configured")
        response = self.model.generate_content(instructions)
        return response.text.strip()
''')

# ======================= MODULES : PIPELINES =======================
write_file("backend/app/modules/pipelines/validators.py", '''
import pandas as pd
from app.core.exceptions import ValidationError

class SchemaValidator:
    REQUIRED_COLUMNS = ["fecha", "producto", "categoria", "cliente", "distrito", "cantidad", "precio_unitario", "total_venta"]

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        normalized_cols = [c.strip().lower().replace(" ", "_") for c in df.columns]
        df.columns = normalized_cols

        missing = [c for c in self.REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValidationError(f"Missing required columns: {missing}")
        return df
''')

write_file("backend/app/modules/pipelines/transformers.py", '''
import pandas as pd

class DataTransformer:
    def transform_and_export(self, df: pd.DataFrame, parquet_export_path: str) -> str:
        df = df.dropna(subset=["fecha", "producto", "total_venta"])
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        df = df.dropna(subset=["fecha"])
        df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce").fillna(0).astype(int)
        df["precio_unitario"] = pd.to_numeric(df["precio_unitario"], errors="coerce").fillna(0.0).astype(float)
        df["total_venta"] = pd.to_numeric(df["total_venta"], errors="coerce").fillna(0.0).astype(float)
        
        for col in ["producto", "categoria", "cliente", "distrito"]:
            df[col] = df[col].astype(str).str.strip()

        df.to_parquet(parquet_export_path, index=False)
        return parquet_export_path
''')

write_file("backend/app/modules/pipelines/services.py", '''
import uuid
import pandas as pd
from app.schemas.responses import UploadPipelineResponse
from app.infrastructure.storage import LocalFileStorage
from app.infrastructure.database import DuckDBRepository
from app.modules.pipelines.validators import SchemaValidator
from app.modules.pipelines.transformers import DataTransformer

class DatasetPipelineService:
    def __init__(self):
        self.storage = LocalFileStorage()
        self.db = DuckDBRepository()
        self.validator = SchemaValidator()
        self.transformer = DataTransformer()

    def process_upload(self, file_stream) -> UploadPipelineResponse:
        dataset_id = str(uuid.uuid4())
        
        # 1. Ingestion: Save Raw
        raw_path = self.storage.save_raw_stream(dataset_id, file_stream)
        
        # Read for pandas pipeline
        df_raw = pd.read_excel(raw_path)
        
        # 2. Validation
        df_validated = self.validator.validate(df_raw)
        
        # 3. Transformation
        processed_path = self.storage.get_processed_filepath(dataset_id)
        self.transformer.transform_and_export(df_validated, processed_path)
        
        # 4. Load to Analytical Storage
        # Map table pointing to parquet. Using specific table name or default 'ventas' depending on use case.
        # For this portfolio context, we register as a global view "ventas_default_sales"
        self.db.load_parquet_to_view(f"ventas", processed_path)
        
        rows = len(df_validated.dropna(subset=["fecha"]))
        return UploadPipelineResponse(
            dataset_id=dataset_id,
            status="processed",
            rows_processed=rows,
            message="Data pipeline executed successfully"
        )
''')

# ======================= MODULES : ANALYTICS =======================
write_file("backend/app/modules/analytics/services.py", '''
from app.infrastructure.database import DuckDBRepository
from app.schemas.responses import AnalyticsSummaryResponse, AnalyticsTrendResponse, AnalyticsRankingResponse

class AnalyticsService:
    def __init__(self):
        self.db = DuckDBRepository()
        # En un sistema multi-tenant, pasaríamos f"ventas_{dataset_id}"
        self.table = "ventas"

    def get_summary(self) -> AnalyticsSummaryResponse:
        try:
            df = self.db.execute_query(f"""
                SELECT 
                    COALESCE(SUM(total_venta), 0) as total_sales,
                    COUNT(*) as total_transactions,
                    COALESCE(AVG(total_venta), 0) as avg_ticket,
                    COUNT(DISTINCT producto) as unique_products,
                    COUNT(DISTINCT cliente) as unique_clients
                FROM {self.table}
            """)
            record = df.to_dict(orient="records")[0]
            return AnalyticsSummaryResponse(**record)
        except Exception:
            return AnalyticsSummaryResponse(total_sales=0, total_transactions=0, avg_ticket=0, unique_products=0, unique_clients=0)

    def get_sales_trend(self) -> list[AnalyticsTrendResponse]:
        try:
            df = self.db.execute_query(f"""
                SELECT strftime(fecha, '%Y-%m') as mes, SUM(total_venta) as total
                FROM {self.table} GROUP BY mes ORDER BY mes
            """)
            return [AnalyticsTrendResponse(**r) for r in df.to_dict(orient="records")]
        except Exception:
            return []

    def get_top_items(self, dimension: str, limit: int = 10) -> list[AnalyticsRankingResponse]:
        try:
            df = self.db.execute_query(f"""
                SELECT {dimension} as nombre, SUM(total_venta) as total
                FROM {self.table} GROUP BY nombre ORDER BY total DESC LIMIT {limit}
            """)
            return [AnalyticsRankingResponse(**r) for r in df.to_dict(orient="records")]
        except Exception:
            return []
''')

# ======================= MODULES : AI QUERY =======================
write_file("backend/app/modules/ai_query/services.py", '''
from app.infrastructure.llm_client import GeminiClient
from app.infrastructure.database import DuckDBRepository
from app.core.security import is_safe_sql_query
from app.core.exceptions import SecurityError
from app.schemas.responses import AskResponse

class NLQueryEngine:
    SCHEMA_HINT = "Tabla: ventas. Columnas: fecha (DATE), producto, categoria, cliente, distrito, cantidad (INT), precio_unitario (DOUBLE), total_venta (DOUBLE)."
    
    def __init__(self):
        self.llm = GeminiClient()
        self.db = DuckDBRepository()

    def translate_and_execute(self, question: str) -> AskResponse:
        prompt_sql = f"Eres un motor NL-to-SQL para DuckDB. Esquema: {self.SCHEMA_HINT}. Pregunta: '{question}'. Retorna unicamente el SQL SELECT valido. Cero explicaciones. Ningún markdown. Empieza con la palabra SELECT."
        
        try:
            sql = self.llm.prompt(prompt_sql).replace("```sql","").replace("```","").strip()
            
            if not is_safe_sql_query(sql):
                raise SecurityError(f"Generated SQL is unsafe: {sql}")
                
            df = self.db.execute_query(sql)
            data_sample = df.head(10).to_dict(orient="records")
            
            prompt_summary = f"Como analista de datos, resume estos resultados {data_sample} para responder '{question}'. Se muy breve y claro."
            summary = self.llm.prompt(prompt_summary)
            
            return AskResponse(question=question, sql_executed=sql, data=data_sample, human_summary=summary)
            
        except Exception as e:
            return AskResponse(question=question, sql_executed="Error", data=[], human_summary=str(e))
''')

# ======================= MODULES : FORECAST =======================
write_file("backend/app/modules/forecast/services.py", '''
import pandas as pd
from prophet import Prophet
from app.infrastructure.database import DuckDBRepository
from app.schemas.responses import ForecastResponse, ForecastItem

class ForecastingEngine:
    def __init__(self):
        self.db = DuckDBRepository()

    def run_monthly_forecast(self) -> ForecastResponse:
        try:
            df = self.db.execute_query("""
                SELECT strftime(fecha, '%Y-%m-01') as ds, SUM(total_venta) as y
                FROM ventas GROUP BY ds ORDER BY ds
            """)
            if len(df) < 2:
                return ForecastResponse(historical=[], forecast=[])
                
            df['ds'] = pd.to_datetime(df['ds'])
            m = Prophet(monthly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
            m.fit(df)
            future = m.make_future_dataframe(periods=6, freq='MS')
            fc = m.predict(future)
            
            historical_data = [{"ds": str(r["ds"].date()), "y": r["y"]} for _, r in df.iterrows()]
            forecast_items = [
                ForecastItem(ds=str(r["ds"].date()), yhat=round(r["yhat"],2), yhat_lower=round(r["yhat_lower"],2), yhat_upper=round(r["yhat_upper"],2))
                for _, r in fc.tail(6).iterrows()
            ]
            return ForecastResponse(historical=historical_data, forecast=forecast_items)
        except Exception:
            return ForecastResponse(historical=[], forecast=[])
''')

# ======================= API ROUTES =======================
write_file("backend/app/api/v1/pipelines.py", '''
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.responses import UploadPipelineResponse
from app.modules.pipelines.services import DatasetPipelineService
from app.core.exceptions import ValidationError

router = APIRouter()

@router.post("/datasets/upload", response_model=UploadPipelineResponse)
def upload_dataset(file: UploadFile = File(...)):
    service = DatasetPipelineService()
    try:
        return service.process_upload(file.file)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
''')

write_file("backend/app/api/v1/analytics.py", '''
from fastapi import APIRouter
from app.modules.analytics.services import AnalyticsService
from app.schemas.responses import AnalyticsSummaryResponse, AnalyticsTrendResponse, AnalyticsRankingResponse

router = APIRouter()

@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_summary():
    return AnalyticsService().get_summary()

@router.get("/sales-by-month", response_model=list[AnalyticsTrendResponse])
def get_sales_trend():
    return AnalyticsService().get_sales_trend()

@router.get("/top-products", response_model=list[AnalyticsRankingResponse])
def get_top_products(limit: int = 10):
    return AnalyticsService().get_top_items(dimension="producto", limit=limit)

@router.get("/top-clients", response_model=list[AnalyticsRankingResponse])
def get_top_clients(limit: int = 10):
    return AnalyticsService().get_top_items(dimension="cliente", limit=limit)
''')

write_file("backend/app/api/v1/ask.py", '''
from fastapi import APIRouter
from app.modules.ai_query.services import NLQueryEngine
from app.schemas.requests import AskRequest
from app.schemas.responses import AskResponse

router = APIRouter()

@router.post("", response_model=AskResponse)
def ask_ai(request: AskRequest):
    engine = NLQueryEngine()
    return engine.translate_and_execute(request.question)
''')

write_file("backend/app/api/v1/forecast.py", '''
from fastapi import APIRouter
from app.modules.forecast.services import ForecastingEngine
from app.schemas.responses import ForecastResponse

router = APIRouter()

@router.get("/monthly", response_model=ForecastResponse)
def generate_monthly_forecast():
    return ForecastingEngine().run_monthly_forecast()
''')

# ======================= MAIN ENTRYPOINT =======================
write_file("backend/app/main.py", '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.v1 import pipelines, analytics, ask, forecast

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, description="Monolito Modular API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registramos routers
app.include_router(pipelines.router, prefix="/api/v1")
app.include_router(pipelines.router, prefix="/upload") # Compatibilidad con front actual
app.include_router(analytics.router, prefix="/api/v1/analytics")
app.include_router(analytics.router, prefix="/dashboard") # Compatibilidad con front actual
app.include_router(ask.router, prefix="/api/v1/ask")
app.include_router(ask.router, prefix="/ask") # Compatibilidad con front actual
app.include_router(forecast.router, prefix="/api/v1/forecast")
app.include_router(forecast.router, prefix="/forecast") # Compatibilidad con front actual

@app.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME}
''')

print("Backend Architectural Refactor Script Generated Succesfully.")
