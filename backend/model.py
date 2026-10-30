import httpx


class ModelError(Exception):
    pass


class OllamaClient:
    def __init__(self, http: httpx.AsyncClient, model: str):
        self.http, self.model = http, model

    async def chat(self, system: str, query: str, schema: dict | None = None) -> str:
        payload = {"model": self.model, "stream": False, "think": False,
                   "messages": [{"role": "system", "content": system},
                                {"role": "user", "content": query}],
                   "options": {"temperature": 0, "num_predict": 1200}}
        if schema:
            payload["format"] = schema
        try:
            response = await self.http.post("/api/chat", json=payload)
            response.raise_for_status()
            content = response.json()["message"]["content"].strip()
            if not content:
                raise ValueError("Empty model response")
            return content
        except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
            raise ModelError("Ollama did not return a valid response. Check the service and configured model.") from exc

    async def available(self) -> bool:
        try:
            response = await self.http.get("/api/tags")
            response.raise_for_status()
            return any(m["name"] == self.model for m in response.json()["models"])
        except (httpx.HTTPError, ValueError, KeyError, TypeError):
            return False
