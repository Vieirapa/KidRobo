from __future__ import annotations

import time
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd

from app.config import (
    AUDIO_CHANNELS,
    AUDIO_RECORD_SECONDS,
    AUDIO_SAMPLE_RATE,
    AUDIO_SILENCE_CHUNKS,
    AUDIO_SILENCE_THRESHOLD,
)


class AudioInput:
    def __init__(self, sample_rate: int = AUDIO_SAMPLE_RATE, channels: int = AUDIO_CHANNELS) -> None:
        self.sample_rate = sample_rate
        self.channels = channels

    def record_to_wav(self, output_path: str | Path, seconds: int = AUDIO_RECORD_SECONDS) -> Path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        frames = sd.rec(
            int(seconds * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
        )
        sd.wait()
        pcm = np.int16(np.clip(frames, -1.0, 1.0) * 32767)

        with wave.open(str(output), "wb") as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(pcm.tobytes())

        return output

    def record_until_silence(self, output_path: str | Path, max_seconds: int = AUDIO_RECORD_SECONDS) -> Path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        chunk_size = int(self.sample_rate * 0.25)
        captured = []
        silent_chunks = 0
        start = time.time()

        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, dtype="float32") as stream:
            while time.time() - start < max_seconds:
                chunk, _ = stream.read(chunk_size)
                captured.append(chunk.copy())
                level = float(np.abs(chunk).mean())

                if level < AUDIO_SILENCE_THRESHOLD:
                    silent_chunks += 1
                else:
                    silent_chunks = 0

                if silent_chunks >= AUDIO_SILENCE_CHUNKS and len(captured) > 2:
                    break

        audio = np.concatenate(captured, axis=0) if captured else np.zeros((1, self.channels), dtype="float32")
        pcm = np.int16(np.clip(audio, -1.0, 1.0) * 32767)

        with wave.open(str(output), "wb") as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(pcm.tobytes())

        return output
