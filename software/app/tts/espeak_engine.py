from __future__ import annotations

import shutil
import subprocess

from app.config import TTS_RATE, TTS_VOICE, TTS_VOLUME


class ESpeakEngine:
    def __init__(self) -> None:
        self.binary = shutil.which("espeak") or shutil.which("espeak-ng")
        if not self.binary:
            raise RuntimeError("espeak/espeak-ng não encontrado no sistema.")

    def say(self, text: str) -> None:
        subprocess.run(
            [
                self.binary,
                "-v",
                TTS_VOICE,
                "-s",
                str(TTS_RATE),
                "-a",
                str(TTS_VOLUME),
                text,
            ],
            check=True,
        )
