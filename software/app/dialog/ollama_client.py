from __future__ import annotations

import json
from urllib import request, error

from app.config import OLLAMA_HOST, OLLAMA_MODEL, SYSTEM_PROMPT


class OllamaClient:
    def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL) -> None:
        self.host = host.rstrip("/")
        self.model = model

    def generate(self, user_text: str) -> str:
        payload = {
            "model": self.model,
            "stream": False,
            "prompt": f"{SYSTEM_PROMPT}\n\nPergunta da criança: {user_text}\nResposta do KidRobo:",
            "options": {
                "temperature": 0.6,
                "num_predict": 80,
            },
        }

        req = request.Request(
            url=f"{self.host}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
                return (data.get("response") or "").strip()
        except error.URLError as exc:
            raise RuntimeError(f"Falha ao acessar Ollama: {exc}") from exc
