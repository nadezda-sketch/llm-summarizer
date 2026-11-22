import asyncio
import logging

import httpx

from config.settings import settings

log = logging.getLogger("llm")

class LLMError(Exception): ...
class LLMTimeout(LLMError): ...
class LLMUnavailable(LLMError): ...

FALLBACK_TEXT = "Сервис временно недоступен. Попробуйте повторить запрос позже."

async def call_llm(messages: list[dict]) -> str:
    # Правильный URL для YandexGPT
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    # Авторизация через Api-Key
    headers = {"Authorization": f"Api-Key {settings.llm_api_key}"}
    
    # Тело запроса для Яндекса
    body = {
        "modelUri": "gpt://b1gi2a6go5l83abi8gdd/yandexgpt-lite/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.2,
            "maxTokens": "2000"
        },
        "messages": messages
    }

    last_err: Exception | None = None
    
    # Цикл повторных попыток (retry)
    for attempt in range(1, settings.llm_max_retries + 2):
        try:
            async with httpx.AsyncClient(timeout=settings.llm_timeout_seconds) as client:
                r = await client.post(url, json=body, headers=headers)
            
            if r.status_code >= 500:
                raise LLMUnavailable(f"upstream {r.status_code}")
            if r.status_code >= 400:
                raise LLMError(f"upstream {r.status_code}: {r.text[:200]}")
            
            data = r.json()
            # Парсинг ответа Яндекса
            return data["result"]["alternatives"][0]["message"]["text"]
            
        except (httpx.TimeoutException, asyncio.TimeoutError) as e:
            last_err = LLMTimeout(str(e))
        except (httpx.HTTPError, LLMUnavailable) as e:
            last_err = LLMUnavailable(str(e))
        except (KeyError, ValueError, IndexError) as e:
            last_err = LLMError(f"bad response: {e}")
            break
            
        log.error("llm attempt failed", extra={"event": "llm_retry", "error": str(last_err)})
        await asyncio.sleep(0.5 * attempt)

    log.error("llm final failure", extra={"event": "llm_failed", "error": str(last_err)})
    raise last_err or LLMUnavailable("unknown")