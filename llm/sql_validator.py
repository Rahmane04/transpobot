# llm/sql_validator.py
import re

MOTS_INTERDITS = [
    "INSERT", "UPDATE", "DELETE", "DROP",
    "ALTER", "CREATE", "TRUNCATE", "REPLACE",
    "GRANT", "REVOKE", "EXEC", "EXECUTE"
]

def is_safe(sql: str) -> bool:
    if not sql:
        return False
    sql_upper = sql.upper().strip()
    # Doit commencer par SELECT
    if not sql_upper.startswith("SELECT"):
        return False
    # Ne doit contenir aucun mot dangereux
    for mot in MOTS_INTERDITS:
        if re.search(r'\b' + mot + r'\b', sql_upper):
            return False
    return True

def clean_sql(sql: str) -> str:
    # Supprime les balises markdown que le LLM pourrait ajouter
    sql = sql.strip()
    sql = re.sub(r"^```sql\s*", "", sql)
    sql = re.sub(r"```$", "", sql)
    sql = sql.strip().rstrip(";")
    return sql
