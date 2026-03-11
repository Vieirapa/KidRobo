from __future__ import annotations

from app.config import ENABLE_OLLAMA
from app.dialog.intents import IntentClassifier
from app.dialog.ollama_client import OllamaClient
from app.dialog.responses import STATIC_RESPONSES
from app.dialog.safety import SafetyFilter


class DialogueManager:
    def __init__(self) -> None:
        self.intent_classifier = IntentClassifier()
        self.safety = SafetyFilter()
        self.ollama = OllamaClient()

    def reply(self, text: str) -> str:
        intent = self.intent_classifier.classify(text)

        if intent.name in STATIC_RESPONSES and intent.name != "fallback":
            return self.safety.sanitize(STATIC_RESPONSES[intent.name])

        if ENABLE_OLLAMA:
            try:
                llm_response = self.ollama.generate(text)
                if llm_response:
                    return self.safety.sanitize(llm_response)
            except RuntimeError:
                pass

        return self.safety.sanitize(STATIC_RESPONSES["fallback"])
