from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IntentResult:
    name: str
    confidence: float = 1.0


class IntentClassifier:
    def classify(self, text: str) -> IntentResult:
        normalized = text.strip().lower()

        greeting_tokens = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]
        robo_markers = [
            "kidrobo", "kid robo", "robô", "robo", "robota", "hobo", "hubo", "jubo", "de robo", "de robô",
            "tudo bem", "tudo bom"
        ]
        if any(token in normalized for token in greeting_tokens):
            if any(marker in normalized for marker in robo_markers):
                return IntentResult("greeting")
            return IntentResult("greeting")
        if normalized in {"kidrobo", "kid robo", "oi kidrobo", "olá kidrobo", "ola kidrobo", "oi robo", "oi robô", "que jubo", "de hobo", "de hubo"}:
            return IntentResult("greeting")
        if "seu nome" in normalized or "como você se chama" in normalized:
            return IntentResult("name")
        if "quantos anos" in normalized or "sua idade" in normalized or "você tem quantos anos" in normalized:
            return IntentResult("age")
        if "quem fez você" in normalized or "quem te fez" in normalized or "quem criou você" in normalized or "quem criou voce" in normalized or "fale sobre você" in normalized or "me fale sobre você" in normalized or "me fale sobre voce" in normalized:
            return IntentResult("creator")
        if "você é de verdade" in normalized or "voce e de verdade" in normalized or "você é um robô de verdade" in normalized or "voce e um robo de verdade" in normalized:
            return IntentResult("real_robot")
        if "você é meu amigo" in normalized or "voce e meu amigo" in normalized or "quer ser meu amigo" in normalized:
            return IntentResult("friend")
        if "maria antonia" in normalized:
            return IntentResult("maria_antonia")
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
        if "você dorme" in normalized or "voce dorme" in normalized:
            return IntentResult("sleep")
        if "você come" in normalized or "voce come" in normalized:
            return IntentResult("eat")
        if "você mora" in normalized or "voce mora" in normalized:
            return IntentResult("home")
        if "você é inteligente" in normalized or "voce e inteligente" in normalized:
            return IntentResult("smart")
        if "você sabe cantar" in normalized or "voce sabe cantar" in normalized:
            return IntentResult("sing")
        if "você sabe dançar" in normalized or "voce sabe dancar" in normalized or "voce sabe dançar" in normalized:
            return IntentResult("dance")
        if "o que tem dentro" in normalized or "o que tem aí dentro" in normalized or "o que tem ai dentro" in normalized:
            return IntentResult("inside")
        if "outra" in normalized and ("curiosidade" in normalized or "conte" in normalized or "me conte" in normalized):
            return IntentResult("another_curiosity")
        if "curiosidade" in normalized or "me conta algo" in normalized or "me fale algo" in normalized:
            return IntentResult("curiosity")
        if "robô" in normalized or "robo" in normalized:
            return IntentResult("robot")
        if "contar" in normalized or "conte até" in normalized or "conte ate" in normalized or "vamos contar" in normalized:
            return IntentResult("count")

        return IntentResult("open_question", confidence=0.6)
