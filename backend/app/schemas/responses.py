from typing import Any
from pydantic import BaseModel
class UploadPipelineResponse(BaseModel): dataset_id: str; status: str; rows_processed: int; message: str
class AnalyticsSummaryResponse(BaseModel): total_ventas: float; total_transacciones: int; ticket_promedio: float; unique_products: int; clientes_unicos: int
class AnalyticsTrendResponse(BaseModel): mes: str; total: float
class AnalyticsRankingResponse(BaseModel): nombre: str; total: float
class AskResponse(BaseModel): question: str; sql_executed: str; data: list[dict[str, Any]]; human_summary: str
class ForecastItem(BaseModel): ds: str; yhat: float; yhat_lower: float; yhat_upper: float
class ForecastResponse(BaseModel): historical: list[dict[str, Any]]; forecast: list[ForecastItem]