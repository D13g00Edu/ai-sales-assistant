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
