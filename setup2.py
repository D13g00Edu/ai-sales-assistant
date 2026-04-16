import os
def d(p,c):
    open(f'c:/Users/diego/Desktop/proyectos/Mlops/backend/app/{p}','w',encoding='utf8').write(c.strip())

d('infrastructure/database.py', '''
import duckdb
from pathlib import Path
from app.core.config import get_settings
class DuckDBRepository:
    def __init__(self):
        s = get_settings()
        Path(s.DUCKDB_PATH).parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(database=s.DUCKDB_PATH, read_only=False)
    def execute_query(self, query: str):
        return self.conn.execute(query).df()
    def load_parquet_to_view(self, view_name: str, parquet_path: str):
        self.conn.execute(f"CREATE OR REPLACE VIEW {view_name} AS SELECT * FROM read_parquet('{parquet_path}')")
''')

d('infrastructure/storage.py', '''
import os, shutil
from app.core.config import get_settings
class LocalFileStorage:
    def __init__(self):
        self.s = get_settings()
        os.makedirs(self.s.DATA_RAW_DIR, exist_ok=True)
        os.makedirs(self.s.DATA_PROCESSED_DIR, exist_ok=True)
    def save_raw_stream(self, dataset_id: str, file_stream) -> str:
        fp = os.path.join(self.s.DATA_RAW_DIR, f'{dataset_id}.xlsx')
        with open(fp, 'wb') as f: shutil.copyfileobj(file_stream, f)
        return fp
    def get_processed_filepath(self, dataset_id: str) -> str:
        return os.path.join(self.s.DATA_PROCESSED_DIR, f'{dataset_id}.parquet')
''')

d('infrastructure/llm_client.py', '''
import google.generativeai as genai
from app.core.config import get_settings
from app.core.exceptions import SecurityError
class GeminiClient:
    def __init__(self):
        self.s = get_settings()
        if self.s.GEMINI_API_KEY: genai.configure(api_key=self.s.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.s.GEMINI_MODEL)
    def prompt(self, txt: str) -> str:
        if not self.s.GEMINI_API_KEY: raise SecurityError('GEMINI API Key is missing')
        return self.model.generate_content(txt).text.strip()
''')

d('modules/pipelines/validators.py', '''
import pandas as pd
from app.core.exceptions import ValidationError
class SchemaValidator:
    REQ = ['fecha', 'producto', 'categoria', 'cliente', 'distrito', 'cantidad', 'precio_unitario', 'total_venta']
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
        missing = [c for c in self.REQ if c not in df.columns]
        if missing: raise ValidationError(f'Columnas faltantes: {missing}')
        return df
''')

d('modules/pipelines/transformers.py', '''
import pandas as pd
class DataTransformer:
    def transform_and_export(self, df: pd.DataFrame, out_path: str) -> str:
        df = df.dropna(subset=['fecha', 'producto', 'total_venta'])
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        df = df.dropna(subset=['fecha'])
        df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce').fillna(0).astype(int)
        df['precio_unitario'] = pd.to_numeric(df['precio_unitario'], errors='coerce').fillna(0.0).astype(float)
        df['total_venta'] = pd.to_numeric(df['total_venta'], errors='coerce').fillna(0.0).astype(float)
        for col in ['producto', 'categoria', 'cliente', 'distrito']:
            df[col] = df[col].astype(str).str.strip()
        df.to_parquet(out_path, index=False)
        return out_path
''')

d('modules/pipelines/services.py', '''
import uuid, pandas as pd
from app.schemas.responses import UploadPipelineResponse
from app.infrastructure.storage import LocalFileStorage
from app.infrastructure.database import DuckDBRepository
from .validators import SchemaValidator
from .transformers import DataTransformer
class DatasetPipelineService:
    def __init__(self):
        self.st, self.db = LocalFileStorage(), DuckDBRepository()
        self.val, self.tr = SchemaValidator(), DataTransformer()
    def process_upload(self, file_stream) -> UploadPipelineResponse:
        did = str(uuid.uuid4())
        raw_path = self.st.save_raw_stream(did, file_stream)
        df_raw = pd.read_excel(raw_path)
        df_val = self.val.validate(df_raw)
        proc_path = self.st.get_processed_filepath(did)
        self.tr.transform_and_export(df_val, proc_path)
        self.db.load_parquet_to_view('ventas', proc_path)
        return UploadPipelineResponse(dataset_id=did, status='processed', rows_processed=len(df_val.dropna(subset=['fecha'])), message='Dataset ingestión exitosa')
''')

# Analytics, Forecast, AI Query

d('modules/analytics/services.py', '''
from app.infrastructure.database import DuckDBRepository
from app.schemas.responses import AnalyticsSummaryResponse, AnalyticsTrendResponse, AnalyticsRankingResponse
class AnalyticsService:
    def __init__(self): self.db, self.tbl = DuckDBRepository(), 'ventas'
    def get_summary(self):
        try:
            df = self.db.execute_query(f"SELECT COALESCE(SUM(total_venta), 0) as total_sales, COUNT(*) as total_transactions, COALESCE(AVG(total_venta), 0) as avg_ticket, COUNT(DISTINCT producto) as unique_products, COUNT(DISTINCT cliente) as unique_clients FROM {self.tbl}")
            return AnalyticsSummaryResponse(**df.to_dict('records')[0])
        except: return AnalyticsSummaryResponse(total_sales=0, total_transactions=0, avg_ticket=0, unique_products=0, unique_clients=0)
    def get_sales_trend(self):
        try: return [AnalyticsTrendResponse(**r) for r in self.db.execute_query(f"SELECT strftime(fecha, '%Y-%m') as mes, SUM(total_venta) as total FROM {self.tbl} GROUP BY mes ORDER BY mes").to_dict('records')]
        except: return []
    def get_top_items(self, dim: str, limit: int=10):
        try: return [AnalyticsRankingResponse(**r) for r in self.db.execute_query(f"SELECT {dim} as nombre, SUM(total_venta) as total FROM {self.tbl} GROUP BY nombre ORDER BY total DESC LIMIT {limit}").to_dict('records')]
        except: return []
''')

d('modules/ai_query/services.py', '''
from app.infrastructure.llm_client import GeminiClient
from app.infrastructure.database import DuckDBRepository
from app.core.security import is_safe_sql_query
from app.core.exceptions import SecurityError
from app.schemas.responses import AskResponse
class NLQueryEngine:
    SCHEMA = "Tabla: ventas. Cols: fecha (DATE), producto, categoria, cliente, distrito, cantidad (INT), precio_unitario (DOUBLE), total_venta (DOUBLE)."
    def __init__(self): self.llm, self.db = GeminiClient(), DuckDBRepository()
    def translate_and_execute(self, q: str):
        try:
            sql = self.llm.prompt(f"AI SQL NL-to-SQL. Esquema: {self.SCHEMA}. Pregunta: '{q}'. Retorna SOLO el SQL SELECT, sin markdown.").replace('```sql','').replace('```','').strip()
            if not is_safe_sql_query(sql): raise SecurityError("Unsafe SQL")
            data = self.db.execute_query(sql).head(10).to_dict('records')
            summary = self.llm.prompt(f"Se breve. Analista resume: {data} para '{q}'")
            return AskResponse(question=q, sql_executed=sql, data=data, human_summary=summary)
        except Exception as e: return AskResponse(question=q, sql_executed="Error", data=[], human_summary=str(e))
''')

d('modules/forecast/services.py', '''
import pandas as pd
from prophet import Prophet
from app.infrastructure.database import DuckDBRepository
from app.schemas.responses import ForecastResponse, ForecastItem
class ForecastingEngine:
    def __init__(self): self.db = DuckDBRepository()
    def run_monthly_forecast(self):
        try:
            df = self.db.execute_query("SELECT strftime(fecha, '%Y-%m-01') as ds, SUM(total_venta) as y FROM ventas GROUP BY ds ORDER BY ds")
            if len(df)<2: return ForecastResponse(historical=[], forecast=[])
            df['ds'] = pd.to_datetime(df['ds'])
            m = Prophet(monthly_seasonality=True, weekly_seasonality=False, daily_seasonality=False).fit(df)
            fc = m.predict(m.make_future_dataframe(periods=6, freq='MS'))
            h = [{"ds": str(r["ds"].date()), "y": r["y"]} for _,r in df.iterrows()]
            f = [ForecastItem(ds=str(r["ds"].date()), yhat=round(r["yhat"],2), yhat_lower=round(r["yhat_lower"],2), yhat_upper=round(r["yhat_upper"],2)) for _,r in fc.tail(6).iterrows()]
            return ForecastResponse(historical=h, forecast=f)
        except Exception: return ForecastResponse(historical=[], forecast=[])
''')

d('api/v1/__init__.py', '')
d('api/__init__.py', '')
d('core/__init__.py', '')
d('schemas/__init__.py', '')

d('api/v1/pipelines.py', '''
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.responses import UploadPipelineResponse
from app.modules.pipelines.services import DatasetPipelineService
from app.core.exceptions import ValidationError
router = APIRouter()
@router.post("/datasets/upload", response_model=UploadPipelineResponse)
def upload_dataset(file: UploadFile = File(...)):
    try: return DatasetPipelineService().process_upload(file.file)
    except ValidationError as e: raise HTTPException(422, str(e.errors or e))
    except Exception as e: raise HTTPException(500, str(e))
''')

d('api/v1/analytics.py', '''
from fastapi import APIRouter
from app.modules.analytics.services import AnalyticsService
from app.schemas.responses import AnalyticsSummaryResponse, AnalyticsTrendResponse, AnalyticsRankingResponse
router = APIRouter()
@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_summary(): return AnalyticsService().get_summary()
@router.get("/sales-by-month", response_model=list[AnalyticsTrendResponse])
def get_sales_trend(): return AnalyticsService().get_sales_trend()
@router.get("/top-products", response_model=list[AnalyticsRankingResponse])
def get_top_products(limit: int = 10): return AnalyticsService().get_top_items("producto", limit)
@router.get("/top-clients", response_model=list[AnalyticsRankingResponse])
def get_top_clients(limit: int = 10): return AnalyticsService().get_top_items("cliente", limit)
''')

d('api/v1/ask.py', '''
from fastapi import APIRouter
from app.modules.ai_query.services import NLQueryEngine
from app.schemas.requests import AskRequest
from app.schemas.responses import AskResponse
router = APIRouter()
@router.post("", response_model=AskResponse)
def ask_ai(request: AskRequest): return NLQueryEngine().translate_and_execute(request.question)
''')

d('api/v1/forecast.py', '''
from fastapi import APIRouter
from app.modules.forecast.services import ForecastingEngine
from app.schemas.responses import ForecastResponse
router = APIRouter()
@router.get("/monthly", response_model=ForecastResponse)
def generate_monthly_forecast(): return ForecastingEngine().run_monthly_forecast()
''')

d('main.py', '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.v1 import pipelines, analytics, ask, forecast
settings = get_settings()
app = FastAPI(title=settings.APP_NAME, description="Modular Monolith API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=[settings.FRONTEND_URL, "*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(pipelines.router, prefix="/api/v1")
app.include_router(pipelines.router, prefix="/upload")
app.include_router(analytics.router, prefix="/api/v1/analytics")
app.include_router(analytics.router, prefix="/dashboard")
app.include_router(ask.router, prefix="/api/v1/ask")
app.include_router(ask.router, prefix="/ask")
app.include_router(forecast.router, prefix="/api/v1/forecast")
app.include_router(forecast.router, prefix="/forecast")
@app.get("/health")
def health(): return {"status": "ok", "app": settings.APP_NAME}
''')

print('All Python modules generated.')
