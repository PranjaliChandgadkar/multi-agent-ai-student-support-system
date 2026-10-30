# Validation — 30 October 2026

Environment: Windows, Python 3.13.15, project `.venv`, existing Ollama at localhost:11434, `granite4.2:3b`.

- Inspected project: five empty directories; no pre-existing files or documentation.
- Queried Ollama `/api/tags`: confirmed the installed Granite model without reinstalling Ollama or pulling models.
- Backend tests passed (5 tests) before frontend implementation.
- Real Granite integration passed before frontend implementation: FastAPI lifecycle and health, Granite classifier, career generation, visa retrieval and structured citation generation. A temporary fictional policy was used; the answer correctly identified the purple enrolment letter and cited `test-policy-1`.
- Initial real tests exposed overcautious routing and missing citation IDs. Explicit classification examples and schema-constrained visa responses corrected these failures.
- Final suite passed: 6 tests, including Streamlit AppTest initial rendering. `pip check` reported no broken requirements. Dependencies are captured in `requirements-lock.txt`.

The integration test uses FastAPI TestClient and real HTTP requests to Ollama. It does not verify external network access or real immigration policy accuracy. Current Starlette emits a deprecation warning about its httpx TestClient adapter; tests pass.

## USA focus update

- Added two curated State Department summaries, a USA student guide, and a source register with explicit coverage gaps.
- Corrected routing instructions to distinguish consular/visa interviews from job interviews.
- Seven tests passed, including retrieval from the shipped source pack.
- `python -m tests.integration_usa` passed against real Granite. F-1 interview preparation cited `us-student-application-1`; DS-160 preparation cited `us-ds160-1`.
- DHS/USCIS pages that could not be retrieved directly were recorded as pending review and excluded from the knowledge base.
