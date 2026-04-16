from app.infrastructure.database import DuckDBRepository
from app.schemas.responses import AnalyticsSummaryResponse, AnalyticsTrendResponse, AnalyticsRankingResponse

class AnalyticsService:
    def __init__(self): self.db, self.tbl = DuckDBRepository(), 'ventas'

    def get_summary(self):
        try:
            df = self.db.execute_query(f"SELECT COALESCE(SUM(total_venta), 0) as total_ventas, COUNT(*) as total_transacciones, COALESCE(AVG(total_venta), 0) as ticket_promedio, COUNT(DISTINCT producto) as unique_products, COUNT(DISTINCT cliente) as clientes_unicos FROM {self.tbl}")
            return AnalyticsSummaryResponse(**df.to_dict('records')[0])
        except: return AnalyticsSummaryResponse(total_ventas=0, total_transacciones=0, ticket_promedio=0, unique_products=0, clientes_unicos=0)

    def get_sales_trend(self):
        try: return [AnalyticsTrendResponse(**r) for r in self.db.execute_query(f"SELECT strftime(fecha, '%Y-%m') as mes, SUM(total_venta) as total FROM {self.tbl} GROUP BY mes ORDER BY mes").to_dict('records')]
        except: return []

    def get_top_items(self, dim: str, limit: int=10):
        try: return [AnalyticsRankingResponse(**r) for r in self.db.execute_query(f"SELECT {dim} as nombre, SUM(total_venta) as total FROM {self.tbl} GROUP BY nombre ORDER BY total DESC LIMIT {limit}").to_dict('records')]
        except: return []
