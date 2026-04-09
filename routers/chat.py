# routers/chat.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text

# get_db sera fourni par le groupe (partie backend)
# En attendant, tu le mock pour tester
try:
    from database import get_db
except ImportError:
    get_db = None

from llm.llm_service import ask_llm

router = APIRouter(prefix="/api/chat", tags=["Chat IA"])

class QuestionRequest(BaseModel):
    question: str

class ChatReponse(BaseModel):
    question: str
    sql: str | None
    explication: str
    resultats: list | None
    error: str | None

@router.post("/", response_model=ChatReponse)
async def chat(body: QuestionRequest, db: Session = Depends(get_db)):
    question = body.question.strip()

    if not question:
        return ChatReponse(question=question, sql=None,
                           explication="Question vide.", resultats=None, error="EMPTY")

    # Appel LLM
    llm = ask_llm(question)

    if llm["error"] or not llm["sql"]:
        return ChatReponse(question=question, sql=None,
                           explication=llm["explication"], resultats=None, error=llm["error"])

    # Exécution SQL sur la vraie base
    try:
        result = db.execute(text(llm["sql"]))
        colonnes = list(result.keys())
        lignes = [dict(zip(colonnes, row)) for row in result.fetchall()]
        return ChatReponse(question=question, sql=llm["sql"],
                           explication=llm["explication"], resultats=lignes, error=None)
    except Exception as e:
        return ChatReponse(question=question, sql=llm["sql"],
                           explication="Erreur SQL.", resultats=None, error=str(e))
