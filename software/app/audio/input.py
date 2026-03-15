from __future__ import annotations

import time
import wave
from collections import deque
from pathlib import Path

import numpy as np
import sounddevice as sd

try:
    import webrtcvad  # type: ignore
except Exception:
    webrtcvad = None

from app.config import (
    AUDIO_CHANNELS,
    AUDIO_RECORD_SECONDS,
    AUDIO_SAMPLE_RATE,
    AUDIO_SILENCE_CHUNKS,
    AUDIO_SILENCE_THRESHOLD,
    AUDIO_USE_VAD,
    AUDIO_VAD_END_FRAMES,
    AUDIO_VAD_FRAME_MS,
    AUDIO_VAD_MODE,
    AUDIO_VAD_PREROLL_FRAMES,
    AUDIO_VAD_START_FRAMES,
)


class AudioInput:
    def __init__(self, sample_rate: int = AUDIO_SAMPLE_RATE, channels: int = AUDIO_CHANNELS) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.use_vad = AUDIO_USE_VAD and webrtcvad is not None
        self.frame_ms = AUDIO_VAD_FRAME_MS
        self.frame_size = int(self.sample_rate * self.frame_ms / 1000)
        self.vad = webrtcvad.Vad(AUDIO_VAD_MODE) if self.use_vad else None

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
        self._write_wav(output, pcm)
        return output

    def record_until_silence(self, output_path: str | Path, max_seconds: int = AUDIO_RECORD_SECONDS) -> Path:
        if self.use_vad:
            return self.record_utterance(output_path, max_seconds=max_seconds)

        if AUDIO_USE_VAD and webrtcvad is None:
            print("[aviso] webrtcvad indisponível neste ambiente; usando detector simples por silêncio.")

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
        self._write_wav(output, pcm)
        return output

    def record_utterance(self, output_path: str | Path, max_seconds: int = AUDIO_RECORD_SECONDS) -> Path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        preroll: deque[np.ndarray] = deque(maxlen=AUDIO_VAD_PREROLL_FRAMES)
        captured: list[np.ndarray] = []
        voiced_started = False
        speech_frames = 0
        silence_frames = 0
        deadline = time.monotonic() + max_seconds

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            blocksize=self.frame_size,
        ) as stream:
            while time.monotonic() < deadline:
                chunk, _ = stream.read(self.frame_size)
                frame = chunk.copy()
                mono = frame.reshape(-1)
                is_speech = self.vad.is_speech(mono.tobytes(), self.sample_rate) if self.vad else False

                if not voiced_started:
                    preroll.append(frame)
                    if is_speech:
                        speech_frames += 1
                    else:
                        speech_frames = 0

                    if speech_frames >= AUDIO_VAD_START_FRAMES:
                        voiced_started = True
                        captured.extend(preroll)
                        silence_frames = 0
                    continue

                captured.append(frame)
                if is_speech:
                    silence_frames = 0
                else:
                    silence_frames += 1
                    if silence_frames >= AUDIO_VAD_END_FRAMES:
                        break

        if not captured:
            audio = np.zeros((self.frame_size, self.channels), dtype=np.int16)
        else:
            audio = np.concatenate(captured, axis=0)

        self._write_wav(output, audio)
        return output

    def _write_wav(self, output: Path, pcm: np.ndarray) -> None:
        pcm = np.asarray(pcm, dtype=np.int16)
        if pcm.ndim == 1:
            pcm = pcm.reshape(-1, self.channels)

        with wave.open(str(output), "wb") as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(pcm.tobytes())
