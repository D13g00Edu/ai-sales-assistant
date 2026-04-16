from fastapi import APIRouter
from app.modules.forecast.services import ForecastingEngine
from app.schemas.responses import ForecastResponse

router = APIRouter()

@router.get("/monthly", response_model=ForecastResponse)
def generate_monthly_forecast(): return ForecastingEngine().run_monthly_forecast()
