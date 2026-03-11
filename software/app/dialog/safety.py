from __future__ import annotations

import re

from app.config import MAX_RESPONSE_CHARS, MAX_RESPONSE_SENTENCES


class SafetyFilter:
    BANNED_PATTERNS = [
        r"arma",
        r"viol[eê]n",
        r"machucar",
        r"sangue",
        r"odio",
        r"ódio",
    ]

    def sanitize(self, text: str) -> str:
        clean = " ".join(text.split())

        for pattern in self.BANNED_PATTERNS:
            if re.search(pattern, clean, flags=re.IGNORECASE):
                return "Vamos falar de algo divertido e seguro. Quer uma curiosidade sobre robôs?"

        sentences = re.split(r"(?<=[.!?])\s+", clean)
        clean = " ".join(sentences[:MAX_RESPONSE_SENTENCES]).strip()

        if len(clean) > MAX_RESPONSE_CHARS:
            clean = clean[: MAX_RESPONSE_CHARS - 3].rstrip() + "..."

        return clean or "Vamos tentar de novo com uma pergunta curtinha?"
