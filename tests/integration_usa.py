"""Real Granite check using the bundled US sources: python -m tests.integration_usa."""
from fastapi.testclient import TestClient
from backend.main import app


def main():
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        for question, source in [
            ("What documents should I prepare for my US F-1 visa interview?", "us-student-application"),
            ("What information should I have ready to complete DS-160 as an F-1 applicant?", "us-ds160"),
        ]:
            response = client.post("/chat", json={"message": question})
            assert response.status_code == 200, response.text
            answer = response.json()
            assert answer["agent"] == "visa", answer
            assert any(c["id"].startswith(source + "-") for c in answer["citations"]), answer
            assert "ds-160" in answer["answer"].lower(), answer
            print(question)
            print(answer["answer"])
            print("Sources:", [c["id"] for c in answer["citations"]], flush=True)
    print("PASS: US visa interview routing and bundled source citations")


if __name__ == "__main__":
    main()
