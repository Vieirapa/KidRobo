from __future__ import annotations

from pathlib import Path

from faster_whisper import WhisperModel

from app.config import STT_COMPUTE_TYPE, STT_DEVICE, STT_MODEL_SIZE


class FasterWhisperEngine:
    def __init__(self) -> None:
        self.model = WhisperModel(
            STT_MODEL_SIZE,
            device=STT_DEVICE,
            compute_type=STT_COMPUTE_TYPE,
        )

    def transcribe_file(self, audio_path: str | Path) -> str:
        segments, _ = self.model.transcribe(str(audio_path), language="pt", vad_filter=True)
        text = " ".join(segment.text.strip() for segment in segments).strip()
        return text
