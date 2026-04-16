def is_safe_sql_query(sql_query: str) -> bool:
    q = sql_query.upper().strip()
    return q.startswith('SELECT') and not any(kw in q for kw in ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'TRUNCATE', 'ALTER'])