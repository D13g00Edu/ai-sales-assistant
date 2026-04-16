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
            sql = self.llm.prompt(f"AI SQL NL-to-SQL. Esquema: {self.SCHEMA}. Pregunta: '{q}'. Retorna SOLO el SQL SELECT, sin markdown.").replace('`sql','').replace('`','').strip()
            if not is_safe_sql_query(sql): raise SecurityError("Unsafe SQL")
            data = self.db.execute_query(sql).head(10).to_dict('records')
            summary = self.llm.prompt(f"Se breve. Analista resume: {data} para '{q}'")
            return AskResponse(question=q, sql_executed=sql, data=data, human_summary=summary)
        except Exception as e: return AskResponse(question=q, sql_executed="Error", data=[], human_summary=str(e))
