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
