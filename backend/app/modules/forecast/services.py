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
