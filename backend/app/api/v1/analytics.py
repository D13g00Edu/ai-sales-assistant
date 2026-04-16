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
