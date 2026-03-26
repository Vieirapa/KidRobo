from __future__ import annotations

from app.config import ENABLE_OLLAMA
from app.dialog.intents import IntentClassifier
from app.dialog.ollama_client import OllamaClient
from app.dialog.responses import FALLBACK_LINES, STATIC_RESPONSES
from app.dialog.safety import SafetyFilter
from app.dialog.school_demo_lines import random_school_demo_fallback


class DialogueManager:
    def __init__(self, school_demo: bool = False) -> None:
        self.school_demo = school_demo
        self.intent_classifier = IntentClassifier()
        self.safety = SafetyFilter()
        self.ollama = OllamaClient()
        self.last_reply = ""

    def _remember(self, text: str, source: str) -> tuple[str, str]:
        self.last_reply = text
        return self.safety.sanitize(text), source

    def reply(self, text: str) -> tuple[str, str]:
        intent = self.intent_classifier.classify(text)

        if intent.name in STATIC_RESPONSES and intent.name not in {"fallback", "open_question"}:
            return self._remember(STATIC_RESPONSES[intent.name], "local")

        if self.school_demo:
            return self._remember(random_school_demo_fallback(last_line=self.last_reply), "school-demo-fallback")

        if ENABLE_OLLAMA:
            try:
                llm_response = self.ollama.generate(text)
                if llm_response:
                    return self._remember(llm_response, "ollama")
            except RuntimeError as exc:
                print(f"[aviso] fallback local após falha no Ollama: {exc}")

        fallback = next((line for line in FALLBACK_LINES if line != self.last_reply), FALLBACK_LINES[0])
        return self._remember(fallback, "fallback")
