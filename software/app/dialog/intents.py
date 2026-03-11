from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IntentResult:
    name: str
    confidence: float = 1.0


class IntentClassifier:
    def classify(self, text: str) -> IntentResult:
        normalized = text.strip().lower()

        if any(token in normalized for token in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]):
            return IntentResult("greeting")
        if "seu nome" in normalized or "como você se chama" in normalized:
            return IntentResult("name")
        if "brinc" in normalized or "jogar" in normalized:
            return IntentResult("play")
        if "curiosidade" in normalized or "me conta algo" in normalized:
            return IntentResult("curiosity")
        if "robô" in normalized or "robo" in normalized:
            return IntentResult("robot")
        if "contar" in normalized or "conte até" in normalized:
            return IntentResult("count")

        return IntentResult("open_question", confidence=0.6)
