## Module LLM - TranspoBot

### Ce que ce module expose
- **Endpoint** : `POST /api/chat/`
- **Body** : `{ "question": "string" }`
- **Réponse** : `{ question, sql, explication, resultats[], error }`

### Ce dont j'ai besoin du backend
- La fonction `get_db` dans `database.py` (session SQLAlchemy)
- La variable d'env `OPENAI_API_KEY` dans le `.env` global

### Ce que l'architecte doit faire dans main.py
```python
from routers.chat import router as chat_router
app.include_router(chat_router)
```

### Tester le module seul (sans le reste)
```bash
pip install openai fastapi sqlalchemy python-dotenv uvicorn pytest
pytest tests/test_llm.py -v # ou  PYTHONPATH=. pytest tests/test_llm.py -v
```
