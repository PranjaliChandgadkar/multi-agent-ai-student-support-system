from fastapi.testclient import TestClient
from backend.main import app
from backend.retrieval import KnowledgeBase
from backend.model import ModelError
import json
import asyncio
from backend.agents import OrchestratorAgent, VisaSupportAgent


def test_empty_knowledge(tmp_path):
    assert KnowledgeBase(tmp_path).search("work hours") == []


def test_api_validation():
    with TestClient(app) as client:
        for message in ("", "   ", "x" * 8001):
            assert client.post("/chat", json={"message": message}).status_code == 422


def test_retrieval(tmp_path):
    (tmp_path / "source.json").write_text(json.dumps({"id": "source", "title": "Renewal",
        "url": "https://example.com", "reviewed": "2026-10-30", "text": "Renewal requires an appointment."}))
    kb = KnowledgeBase(tmp_path)
    assert kb.search("renewal appointment")[0].id == "source-1"
    assert kb.search("unrelated interviews") == []


def test_model_failure_returns_502():
    class Broken:
        async def run(self, query):
            raise ModelError("Service unavailable")
    with TestClient(app) as client:
        app.state.orchestrator = Broken()
        assert client.post("/chat", json={"message": "CV help"}).status_code == 502


def test_visa_rejects_invented_citation(tmp_path):
    (tmp_path / "source.json").write_text(json.dumps({"id": "source", "title": "Renewal",
        "url": "https://example.com", "reviewed": "2026-10-30", "text": "Renewal requires an appointment."}))
    class FakeModel:
        model = "test"
        async def chat(self, *args):
            return json.dumps({"answer": "Renewal is automatic [invented].", "source_ids": ["invented"]})
    result = asyncio.run(VisaSupportAgent(FakeModel(), KnowledgeBase(tmp_path)).run("renewal"))
    assert not result.citations
    assert "could not" in result.answer


def test_us_source_retrieval():
    from backend.config import Settings
    kb = KnowledgeBase(Settings().knowledge_dir)
    assert kb.search("DS-160 SEVIS ID")[0].id.startswith("us-ds160-")
    assert any(c.id.startswith("us-student-application-") for c in kb.search("F-1 interview documents"))
