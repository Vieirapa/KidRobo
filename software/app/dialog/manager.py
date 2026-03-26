from __future__ import annotations

from app.config import ENABLE_OLLAMA
from app.dialog.intents import IntentClassifier
from app.dialog.ollama_client import OllamaClient
from app.dialog.responses import FALLBACK_LINES, STATIC_RESPONSES
from app.dialog.safety import SafetyFilter
from app.dialog.school_demo_lines import all_school_demo_fallback_lines, random_school_demo_fallback


class DialogueManager:
    def __init__(self, school_demo: bool = False) -> None:
        self.school_demo = school_demo
        self.intent_classifier = IntentClassifier()
        self.safety = SafetyFilter()
        self.ollama = OllamaClient()
        self.recent_replies: list[str] = []

    def _remember(self, text: str, source: str) -> tuple[str, str]:
        self.recent_replies.append(text)
        self.recent_replies = self.recent_replies[-5:]
        return self.safety.sanitize(text), source

    def _pick_general_fallback(self) -> str:
        all_fallbacks = [line for group in FALLBACK_LINES.values() for line in group]
        recent = set(self.recent_replies)
        available = [line for line in all_fallbacks if line not in recent]
        pool = available or all_fallbacks
        return pool[0] if len(pool) == 1 else __import__("random").choice(pool)

    def reply(self, text: str) -> tuple[str, str]:
        intent = self.intent_classifier.classify(text)

        if intent.name in STATIC_RESPONSES and intent.name not in {"fallback", "open_question"}:
            return self._remember(STATIC_RESPONSES[intent.name], "local")

        if self.school_demo:
            recent_demo_lines = [line for line in self.recent_replies if line in all_school_demo_fallback_lines()]
            return self._remember(random_school_demo_fallback(recent_lines=recent_demo_lines[-5:]), "school-demo-fallback")

        if ENABLE_OLLAMA:
            try:
                llm_response = self.ollama.generate(text)
                if llm_response:
                    return self._remember(llm_response, "ollama")
            except RuntimeError as exc:
                print(f"[aviso] fallback local após falha no Ollama: {exc}")

        return self._remember(self._pick_general_fallback(), "fallback")
