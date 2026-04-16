import pandas as pd
from app.core.exceptions import ValidationError

class SchemaValidator:
    REQ = ['fecha', 'producto', 'categoria', 'cliente', 'distrito', 'cantidad', 'precio_unitario', 'total_venta']
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
        missing = [c for c in self.REQ if c not in df.columns]
        if missing: raise ValidationError(f'Columnas faltantes: {missing}')
        return df
