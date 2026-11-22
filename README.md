markdown
# LLM Summarizer (YandexGPT)

Production-like сервис для суммаризации текста с использованием YandexGPT. 
Реализован на FastAPI с разделением на слои, структурированным логированием, TTL-кешем и обработкой ошибок.

## 🏗 Архитектура проекта
Проект разделен на независимые слои для обеспечения масштабируемости и тестируемости:
- `api/` — HTTP-слой (FastAPI, Pydantic-валидация).
- `services/` — Бизнес-логика (пайплайн обработки, пост-обработка).
- `llm/` — Работа с моделью (формирование промптов, клиент с таймаутами и retry).
- `config/` — Управление конфигурацией (чтение переменных окружения).
- `infra/` — Инфраструктурные компоненты (JSON-логирование, TTL-кеш).
- `tests/` — Автотесты (pytest).

## 🚀 Быстрый запуск

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```bash
   git clone https://github.com/nadezda-sketch/llm-summarizer.git
   cd llm-summarizer
Создайте и активируйте виртуальное окружение:

bash
python -m venv .venv
source .venv/bin/activate  # Для Windows: .venv\Scripts\activate
Установите зависимости:

bash
pip install -r requirements.txt
Настройте переменные окружения:

bash
cp .env.example .env
Откройте .env и впишите ваш LLM_API_KEY (секретный ключ Yandex Cloud) и LLM_MODEL (с указанием вашего Folder ID).

Запустите сервис:

bash
uvicorn main:app --reload
Сервис будет доступен по адресу: http://localhost:8000. Документация API (Swagger UI): http://localhost:8000/docs.

📡 Использование API
Эндпоинт: POST /summarize

Пример запроса (curl):

bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Искусственный интеллект — это область информатики...", "max_sentences": 2}'
Успешный ответ (200 OK):

json
{
  "summary": "Искусственный интеллект — область информатики...",
  "cached": false,
  "model": "gpt://.../yandexgpt-lite/latest",
  "request_id": "f20ac3c4-246f-484d-aa84-44c92c7139b2"
}
(При повторном запросе с тем же текстом вернется "cached": true).

Ошибка валидации (422 Unprocessable Entity):
Возвращается, если текст пустой или превышает допустимую длину.

Fallback (200 OK):
Если YandexGPT недоступен или возвращает ошибку, сервис не падает, а возвращает заглушку с "fallback": true.

⚙️ Конфигурация (.env)
Все настройки вынесены в переменные окружения (см. .env.example):

LLM_API_KEY — секретный ключ Yandex Cloud (не хранится в репозитории).

LLM_MODEL — URI модели (например, gpt://<folder_id>/yandexgpt-lite/latest).

LLM_TIMEOUT_SECONDS — таймаут запроса к LLM.

CACHE_TTL_SECONDS — время жизни кеша.

🧪 Тестирование и CI
Проект покрыт тестами (успешные сценарии, валидация, кеш, fallback).
Запуск тестов локально:

bash
pytest -q
В проекте настроен CI (GitHub Actions), который при каждом пуше автоматически запускает линтер (Ruff), тесты (Pytest) и проверку сборки.
