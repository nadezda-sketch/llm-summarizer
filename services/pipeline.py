import hashlib
import logging
import time

from config.settings import settings
from infra.cache import TTLCache
from llm.client import FALLBACK_TEXT, LLMError, call_llm
from llm.prompts import build_messages
from services.postprocess import clean, is_valid

log = logging.getLogger("pipeline")
cache = TTLCache(settings.cache_ttl_seconds, settings.cache_max_size)

def cache_key(text: str, max_sentences: int) -> str:
    h = hashlib.sha256(f"{max_sentences}|{text}".encode()).hexdigest()
    return h

async def summarize(text: str, max_sentences: int, request_id: str) -> dict:
    started = time.time()
    key = cache_key(text, max_sentences)
    cached = cache.get(key)
    if cached is not None:
        log.info("cache hit", extra={"event": "cache_hit", "request_id": request_id, "cache": "hit"})
        return {"summary": cached, "cached": True, "model": settings.llm_model}

    log.info("cache miss", extra={"event": "cache_miss", "request_id": request_id, "cache": "miss"})

    messages = build_messages(text, max_sentences)
    log.info("prompt built", extra={"event": "prompt_built", "request_id": request_id})

    try:
        raw = await call_llm(messages)
        log.info("llm responded", extra={"event": "llm_ok", "request_id": request_id,
                                         "latency_ms": int((time.time()-started)*1000)})
        summary = clean(raw)
        if not is_valid(summary):
            raise LLMError("empty or too short response")
    except LLMError as e:
        log.error("llm failed -> fallback", extra={"event": "fallback", "request_id": request_id, "error": str(e)})
        return {"summary": FALLBACK_TEXT, "cached": False, "model": settings.llm_model, "fallback": True}

    cache.set(key, summary)
    return {"summary": summary, "cached": False, "model": settings.llm_model}