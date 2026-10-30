# Multi-Agent AI Student Support System

Native Windows Python application using FastAPI, Streamlit and a custom Python orchestrator. All three agents use the installed `granite4.2:3b` through Ollama. No WSL or agent framework is required.

## Project background

This project was originally intended to use IBM watsonx. This implementation runs locally on Windows, using IBM Granite through the Ollama API instead of the IBM watsonx cloud service. The orchestrator, visa support and career support agents all use the local model; no IBM watsonx account or API credentials are required.

## Setup in PowerShell

Run from this project directory. The `.venv` environment is already provisioned in this workspace; these commands also reproduce it on another Windows machine with Python installed.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Activation is optional; using the explicit interpreter avoids PowerShell execution policy changes. Ollama must already be running on `http://localhost:11434` with `granite4.2:3b` installed.

For the exact validated dependency versions, install with `-r requirements-lock.txt` instead.

## Run

Backend, in one PowerShell terminal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Frontend, in a second terminal in the same project:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py --server.address 127.0.0.1
```

Open `http://localhost:8501`. API documentation is at `http://127.0.0.1:8000/docs`. `GET /health` checks model availability; `POST /chat` accepts `{"message":"Help me prepare for an interview"}` and returns `agent`, `answer`, `citations` and `model`.

Optional environment variables: `SUPPORT_OLLAMA_URL`, `SUPPORT_MODEL`, `SUPPORT_TIMEOUT`, `SUPPORT_KNOWLEDGE_DIR`, and `SUPPORT_API_URL` (frontend). Backend settings may also go in a local `.env` file. Restart after changes.

## Knowledge and behavior

Visa support now focuses on international students applying to study in the USA, initially F-1. Two reviewed State Department summaries cover application preparation and DS-160. See [the USA student guide](docs/USA_STUDENT_GUIDE.md), [source register](docs/USA_SOURCE_REGISTER.md), and `data/visa/README.md` for scope and source ingestion. Employment, status and travel rules are not yet covered. Restart FastAPI after source changes. Retrieval runs locally without an extra embedding model. The visa agent abstains on missing evidence or invalid citations. Citation presence does not guarantee factual entailment; review sources and answers before real immigration decisions.

The orchestrator asks Granite to choose visa, career or clarification using structured JSON. Mixed questions ask the student to separate topics. The career agent supplies CV, job search and interview guidance. This initial version handles each query independently; the UI displays history but does not send prior turns to the model. No authentication, rate limiting or durable conversation storage is included; keep it on localhost. Avoid entering sensitive personal information.

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m tests.integration_granite
.\.venv\Scripts\python.exe -m tests.integration_usa
```

The second command invokes real Granite through the API application's lifecycle. It checks model availability, both specialist routes, career generation, and visa grounding with a temporary fictional policy. It does not install sources or download models. Allow several minutes on a CPU.

The third command tests US visa-interview routing and citations from the bundled State Department sources using real Granite.
