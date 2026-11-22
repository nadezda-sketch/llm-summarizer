# LLM Summarizer

End-to-end сервис суммаризации текста через LLM. Production-like: layered architecture,
env-конфигурации, структурированные логи, TTL-кеш, fallback, CI.

## Архитектура
```
api/        HTTP-слой (FastAPI)
services/   бизнес-логика (pipeline, postprocess)
llm/        формирование промпта + вызов модели (timeout, retry, fallback)
config/     pydantic-settings, чтение env
infra/      логирование (JSON), TTL-кеш
tests/      pytest
```

## Запуск
```bash
git clone <repo> && cd llm-summarizer
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # вписать LLM_API_KEY
uvicorn main:app --reload
```

## API
`POST /summarize`

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Длинный текст...", "max_sentences": 3}'
```

Успех (200):
```json
{"summary": "...", "cached": false, "model": "gpt-4o-mini", "request_id": "..."}
```

Ошибка валидации (422): `{"detail": [...]}`.

Fallback (200, `fallback: true`) — при недоступности LLM.

## Конфигурация
См. `.env.example`. Секреты только в `.env`, `.env` в `.gitignore`.

## Тестирование
`pytest -q` — сценарии: валидный запрос, ошибка валидации, fallback, кеш.
Подробности — в `TESTING.md`.