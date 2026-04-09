# tests/test_llm.py
from llm.sql_validator import is_safe, clean_sql
from llm.llm_service import ask_llm

# Tests du validateur (pas besoin de clé API)
def test_select_ok():
    assert is_safe("SELECT * FROM trajets") == True

def test_delete_bloque():
    assert is_safe("DELETE FROM trajets") == False

def test_drop_bloque():
    assert is_safe("DROP TABLE vehicules") == False

def test_injection_bloque():
    assert is_safe("SELECT * FROM trajets; DROP TABLE trajets") == False

def test_clean_markdown():
    assert clean_sql("```sql\nSELECT * FROM trajets\n```") == "SELECT * FROM trajets"

def test_clean_semicolon():
    assert clean_sql("SELECT * FROM trajets;") == "SELECT * FROM trajets"

# Tests LLM réels (nécessite OPENAI_API_KEY dans .env)
def test_question_trajets_semaine():
    r = ask_llm("Combien de trajets cette semaine ?")
    assert r["error"] is None
    assert r["sql"].upper().startswith("SELECT")
    assert "trajets" in r["sql"].lower()

def test_question_chauffeur_incidents():
    r = ask_llm("Quel chauffeur a le plus d'incidents ce mois ?")
    assert "incidents" in r["sql"].lower()
    assert "chauffeurs" in r["sql"].lower()

def test_question_vehicules_maintenance():
    r = ask_llm("Quels véhicules sont en maintenance ?")
    assert "vehicules" in r["sql"].lower()

def test_question_hors_base():
    r = ask_llm("Bonjour, comment ça va ?")
    assert r["sql"] is None  # Pas de SQL pour cette question
