from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_valid(monkeypatch):
    async def fake(*a, **k): return "Краткий корректный ответ модели для теста."
    monkeypatch.setattr("services.pipeline.call_llm", fake)
    r = client.post("/summarize", json={"text": "Тестовый текст достаточной длины."})
    assert r.status_code == 200
    assert r.json()["summary"].startswith("Краткий")

def test_validation_empty():
    r = client.post("/summarize", json={"text": ""})
    assert r.status_code == 422

def test_validation_too_long():
    r = client.post("/summarize", json={"text": "x" * 20000})
    assert r.status_code == 422

def test_fallback(monkeypatch):
    from llm.client import LLMUnavailable
    async def boom(*a, **k): raise LLMUnavailable("down")
    monkeypatch.setattr("services.pipeline.call_llm", boom)
    r = client.post("/summarize", json={"text": "Текст для проверки fallback."})
    assert r.status_code == 200
    assert r.json()["fallback"] is True