from fastapi import FastAPI

from api.routes import router
from config.settings import settings
from infra.logging import setup_logging

setup_logging(settings.log_level)
app = FastAPI(title="LLM Summarizer", version="1.0.0")
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}