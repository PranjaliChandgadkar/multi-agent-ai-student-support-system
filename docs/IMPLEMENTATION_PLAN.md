# Implementation plan

1. Inspect project and verify the existing Windows Ollama service (completed).
2. Create a Windows virtual environment and install Python application dependencies.
3. Implement a shared asynchronous Ollama client, typed API contracts, Granite query classifier, visa RAG agent and career agent. Use local lexical retrieval so no embedding model download is needed.
4. Add source files with explicit metadata and a reproducible test fixture; empty knowledge bases must abstain. Keep policy content user supplied rather than inventing current visa rules.
5. Test API behavior and run an opt-in real Granite integration test for both routes before frontend work.
6. Build a Streamlit chat interface with agent labels, citation display and backend error handling.
7. Document PowerShell setup, execution, knowledge ingestion and limitations.

## Architecture

Streamlit -> FastAPI -> custom Python orchestrator -> Granite routing -> visa or career agent -> shared Ollama client -> granite4.2:3b.

Visa retrieval uses paragraph chunks and normalized lexical relevance. Each JSON source supplies id, title, URL, reviewed date and text. The response exposes only retrieved citations actually referenced by the model. This is a local prototype, with no authentication or persistent student conversations; bind services to loopback.
