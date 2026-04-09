# llm/llm_service.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from .prompt_builder import build_messages
from .sql_validator import is_safe, clean_sql

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(question: str) -> dict:
    """
    Prend une question en langage naturel.
    Retourne : { sql, explication, error }
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=build_messages(question),
            temperature=0,
            max_tokens=500,
            response_format={"type": "json_object"}
        )

        contenu = response.choices[0].message.content
        parsed = json.loads(contenu)

        sql = parsed.get("sql", None)
        explication = parsed.get("explication", "")

        if sql:
            sql = clean_sql(sql)
            if not is_safe(sql):
                return {
                    "sql": None,
                    "explication": "⚠️ Requête bloquée pour des raisons de sécurité.",
                    "error": "UNSAFE_QUERY"
                }

        return {"sql": sql, "explication": explication, "error": None}

    except json.JSONDecodeError:
        return {"sql": None, "explication": "Erreur de parsing JSON.", "error": "JSON_ERROR"}
    except Exception as e:
        return {"sql": None, "explication": f"Erreur : {str(e)}", "error": str(e)}
