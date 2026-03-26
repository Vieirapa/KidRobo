from __future__ import annotations

from app.config import ENABLE_OLLAMA
from app.dialog.intents import IntentClassifier
from app.dialog.ollama_client import OllamaClient
import random

from app.dialog.responses import CURIOSITY_LINES, ENGINEERING_FIELD_LINES, ENGINEER_PROFESSION_LINES, FALLBACK_LINES, JOKE_LINES, STATIC_RESPONSES
from app.dialog.safety import SafetyFilter
from app.dialog.school_demo_lines import all_school_demo_fallback_lines, random_school_demo_fallback


class DialogueManager:
    def __init__(self, school_demo: bool = False, demo_guardrails: bool = False) -> None:
        self.school_demo = school_demo
        self.demo_guardrails = demo_guardrails
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
        return pool[0] if len(pool) == 1 else random.choice(pool)

    def _pick_rotating_line(self, lines: list[str]) -> str:
        recent = set(self.recent_replies)
        available = [line for line in lines if line not in recent]
        pool = available or lines
        return pool[0] if len(pool) == 1 else random.choice(pool)

    def _looks_bad_for_demo(self, user_text: str, reply: str) -> bool:
        normalized_user = user_text.strip().lower()
        normalized_reply = reply.strip().lower()

        if not normalized_reply:
            return True

        suspicious_fragments = [
            "aqui está a resposta",
            "resposta rápida e lúdica",
            "agradeço sua pergunta",
            "visão bastante geral",
            "claro, agradeço",
            "pergunta da criança",
            "kidrobo:",
            "o que você gostaria de saber",
            "você acha que pode",
            "vamos explorar",
            "lindo, roupas são ótimas",
            "claro, a gente dá",
        ]
        if any(fragment in normalized_reply for fragment in suspicious_fragments):
            return True

        weird_starts = [
            "olá, pequena",
            "olá, querida",
            "obrigado, criança",
            "a corda roubou",
            "uma perna e um pavo",
            "sim, o engenheiro é",
            "olá! você saiu",
            "aí, bode",
            "eu sou um robô inteligente",
        ]
        if any(normalized_reply.startswith(fragment) for fragment in weird_starts):
            return True

        if len(normalized_reply.split()) < 4:
            return True

        if normalized_user and normalized_reply == normalized_user:
            return True

        return False

    def reply(self, text: str) -> tuple[str, str]:
        intent = self.intent_classifier.classify(text)

        if intent.name == "joke":
            return self._remember(self._pick_rotating_line(JOKE_LINES), "local")

        if intent.name == "engineer_profession":
            return self._remember(self._pick_rotating_line(ENGINEER_PROFESSION_LINES), "local")

        if intent.name == "engineering_field":
            return self._remember(self._pick_rotating_line(ENGINEERING_FIELD_LINES), "local")

        if intent.name in {"curiosity", "another_curiosity"}:
            return self._remember(self._pick_rotating_line(CURIOSITY_LINES), "local")

        if intent.name in STATIC_RESPONSES and intent.name not in {"fallback", "open_question"}:
            return self._remember(STATIC_RESPONSES[intent.name], "local")

        if self.school_demo:
            recent_demo_lines = [line for line in self.recent_replies if line in all_school_demo_fallback_lines()]
            return self._remember(random_school_demo_fallback(recent_lines=recent_demo_lines[-5:]), "school-demo-fallback")

        if ENABLE_OLLAMA:
            try:
                llm_response = self.ollama.generate(text)
                if llm_response:
                    if self.demo_guardrails and self._looks_bad_for_demo(text, llm_response):
                        print("[aviso] resposta do Ollama rejeitada pelos guardrails da demo; usando fallback local")
                    else:
                        return self._remember(llm_response, "ollama")
            except RuntimeError as exc:
                print(f"[aviso] fallback local após falha no Ollama: {exc}")

        return self._remember(self._pick_general_fallback(), "fallback")
