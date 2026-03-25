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
        if "quantos anos" in normalized or "sua idade" in normalized or "você tem quantos anos" in normalized:
            return IntentResult("age")
        if "o que você faz" in normalized or "para que você serve" in normalized or "o que voce faz" in normalized:
            return IntentResult("purpose")
        if "brinc" in normalized or "jogar" in normalized:
            return IntentResult("play")
        if "piada" in normalized or "engraçad" in normalized or "engracad" in normalized:
            return IntentResult("joke")
        if "dinossauro" in normalized or "dinossauros" in normalized:
            return IntentResult("dinosaur")
        if "espaço" in normalized or "espaco" in normalized or "planeta" in normalized or "estrel" in normalized:
            return IntentResult("space")
        if "animal" in normalized or "bicho" in normalized:
            return IntentResult("animal")
        if "cor favorita" in normalized or "qual é sua cor" in normalized or "qual e sua cor" in normalized:
            return IntentResult("color")
        if "outra" in normalized and ("curiosidade" in normalized or "conte" in normalized or "me conte" in normalized):
            return IntentResult("another_curiosity")
        if "curiosidade" in normalized or "me conta algo" in normalized or "me fale algo" in normalized:
            return IntentResult("curiosity")
        if "robô" in normalized or "robo" in normalized:
            return IntentResult("robot")
        if "contar" in normalized or "conte até" in normalized or "conte ate" in normalized or "vamos contar" in normalized:
            return IntentResult("count")

        return IntentResult("open_question", confidence=0.6)
