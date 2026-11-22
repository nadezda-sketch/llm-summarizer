import logging
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from config.settings import settings
from services.pipeline import summarize

log = logging.getLogger("api")
router = APIRouter()

class SummarizeIn(BaseModel):
    text: str = Field(..., min_length=1, max_length=settings.max_input_chars)
    max_sentences: int = Field(settings.default_max_sentences, ge=1, le=10)

@router.post("/summarize")
async def summarize_endpoint(payload: SummarizeIn):
    request_id = str(uuid.uuid4())
    log.info("request received", extra={"event": "request_in", "request_id": request_id})
    try:
        result = await summarize(payload.text, payload.max_sentences, request_id)
    except Exception as e:
        log.error("internal error", extra={"event": "internal_error", "request_id": request_id, "error": str(e)})
        raise HTTPException(status_code=500, detail={"request_id": request_id, "error": "internal"})
    result["request_id"] = request_id
    return result