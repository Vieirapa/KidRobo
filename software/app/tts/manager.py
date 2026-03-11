from __future__ import annotations

from app.config import ENABLE_TTS, TTS_ENGINE
from app.tts.espeak_engine import ESpeakEngine


class TTSManager:
    def __init__(self) -> None:
        self.enabled = ENABLE_TTS
        self.engine_name = TTS_ENGINE
        self.engine = None

        if self.enabled and self.engine_name == "espeak":
            self.engine = ESpeakEngine()

    def say(self, text: str) -> None:
        if not self.enabled:
            return
        if not self.engine:
            raise RuntimeError("Nenhum engine de TTS disponível.")
        self.engine.say(text)
