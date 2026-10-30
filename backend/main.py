from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, HTTPException, Request
from backend.agents import OrchestratorAgent
from backend.config import Settings
from backend.model import ModelError, OllamaClient
from backend.retrieval import KnowledgeBase
from backend.schemas import Answer, Query


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    async with httpx.AsyncClient(base_url=settings.ollama_url, timeout=settings.timeout, trust_env=False) as http:
        app.state.model = OllamaClient(http, settings.model)
        app.state.orchestrator = OrchestratorAgent(app.state.model, KnowledgeBase(settings.knowledge_dir))
        yield


app = FastAPI(title="Student Support System", lifespan=lifespan)


@app.get("/health")
async def health(request: Request):
    if not await request.app.state.model.available():
        raise HTTPException(503, "Configured Ollama model is unavailable")
    return {"status": "ok", "model": request.app.state.model.model,
            "visa_chunks": len(request.app.state.orchestrator.visa.knowledge.chunks)}


@app.post("/chat", response_model=Answer)
async def chat(query: Query, request: Request):
    try:
        return await request.app.state.orchestrator.run(query.message)
    except ModelError as exc:
        raise HTTPException(502, str(exc)) from exc
