from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.v1 import pipelines, analytics, ask, forecast

settings = get_settings()
app = FastAPI(title=settings.APP_NAME, description="Modular Monolith API", version="2.0.0")

app.add_middleware(CORSMiddleware, allow_origins=[settings.FRONTEND_URL, "*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(pipelines.router, prefix="/api/v1/datasets/upload")
app.include_router(pipelines.router, prefix="/upload")
app.include_router(analytics.router, prefix="/api/v1/analytics")
app.include_router(analytics.router, prefix="/dashboard")
app.include_router(ask.router, prefix="/api/v1/ask")
app.include_router(ask.router, prefix="/ask")
app.include_router(forecast.router, prefix="/api/v1/forecast")
app.include_router(forecast.router, prefix="/forecast")

@app.get("/health")
def health(): return {"status": "ok", "app": settings.APP_NAME}
