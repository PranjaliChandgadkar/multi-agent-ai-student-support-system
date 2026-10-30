"""Opt-in real model test: python -m tests.integration_granite."""
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from fastapi.testclient import TestClient
from backend.main import app


def main():
    # A synthetic policy verifies grounding, never deployed as actual visa advice.
    with TemporaryDirectory() as directory:
        Path(directory, "fixture.json").write_text(json.dumps({
            "id": "test-policy", "title": "Fictional Testland student visa policy",
            "url": "https://example.com/test-policy", "reviewed": "2026-10-30",
            "text": "Fictional Testland integration test only: students renewing a student visa must book an appointment with the campus visa office and bring their purple enrolment letter. This is synthetic test data, not real immigration guidance."
        }), encoding="utf-8")
        previous = os.environ.get("SUPPORT_KNOWLEDGE_DIR")
        os.environ["SUPPORT_KNOWLEDGE_DIR"] = directory
        try:
            with TestClient(app) as client:
                assert client.get("/health").status_code == 200
                for query, agent in [
                    ("How should I prepare for a graduate software engineering interview?", "career"),
                    ("In the fictional Testland test policy, what letter must I bring to renew my student visa?", "visa")]:
                    response = client.post("/chat", json={"message": query})
                    assert response.status_code == 200, response.text
                    result = response.json()
                    assert result["agent"] == agent, result
                    assert len(result["answer"]) > 30, result
                    if agent == "visa":
                        assert result["citations"], result
                        assert "purple" in result["answer"].lower(), result
                    print(json.dumps(result, indent=2))
        finally:
            if previous is None:
                os.environ.pop("SUPPORT_KNOWLEDGE_DIR", None)
            else:
                os.environ["SUPPORT_KNOWLEDGE_DIR"] = previous
    print("PASS: real Granite routing, career generation and cited visa retrieval")


if __name__ == "__main__":
    main()
