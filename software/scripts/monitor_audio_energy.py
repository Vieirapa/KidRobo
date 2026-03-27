#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time
from statistics import mean

import numpy as np
import sounddevice as sd

from app.config import AUDIO_CHANNELS, AUDIO_FALLBACK_SAMPLE_RATES, AUDIO_SAMPLE_RATE


def resolve_sample_rate(preferred_rate: int, channels: int) -> int:
    candidate_rates = [preferred_rate, *AUDIO_FALLBACK_SAMPLE_RATES]
    seen: set[int] = set()

    for rate in candidate_rates:
        if rate in seen:
            continue
        seen.add(rate)
        try:
            sd.check_input_settings(samplerate=rate, channels=channels, dtype="float32")
            if rate != preferred_rate:
                print(f"[aviso] sample rate {preferred_rate} Hz não suportado; usando {rate} Hz.")
            return rate
        except Exception:
            continue

    device_info = sd.query_devices(kind="input")
    fallback_rate = int(device_info.get("default_samplerate") or preferred_rate)
    if fallback_rate != preferred_rate:
        print(f"[aviso] sample rate {preferred_rate} Hz não suportado; usando {fallback_rate} Hz.")
    return fallback_rate


def format_stats(values: list[float]) -> str:
    if not values:
        return "sem dados"
    arr = np.array(values, dtype=np.float32)
    return (
        f"min={arr.min():.5f} avg={arr.mean():.5f} "
        f"max={arr.max():.5f} p95={np.percentile(arr, 95):.5f}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitora a energia real do áudio capturado pelo KidRobo")
    parser.add_argument("--seconds", type=float, default=20.0, help="Tempo total de monitoramento")
    parser.add_argument("--chunk-ms", type=float, default=250.0, help="Tamanho do chunk em ms")
    parser.add_argument("--speak-after", type=float, default=8.0, help="Momento em que a pessoa deve começar a falar")
    parser.add_argument("--threshold", type=float, default=0.025, help="Threshold que queremos comparar")
    args = parser.parse_args()

    channels = AUDIO_CHANNELS
    sample_rate = resolve_sample_rate(AUDIO_SAMPLE_RATE, channels)
    chunk_frames = max(1, int(sample_rate * (args.chunk_ms / 1000.0)))

    print("=== monitor de energia do áudio ===")
    print(f"sample_rate={sample_rate}Hz channels={channels} chunk_frames={chunk_frames}")
    print(f"threshold de referência={args.threshold:.5f}")
    print(f"fique em silêncio até ~{args.speak_after:.1f}s, depois fale por alguns segundos")
    print()

    all_levels: list[float] = []
    silent_levels: list[float] = []
    speech_levels: list[float] = []

    start = time.monotonic()
    with sd.InputStream(samplerate=sample_rate, channels=channels, dtype="float32") as stream:
        while True:
            elapsed = time.monotonic() - start
            if elapsed >= args.seconds:
                break

            chunk, _ = stream.read(chunk_frames)
            level = float(np.abs(chunk).mean())
            peak = float(np.abs(chunk).max())
            all_levels.append(level)

            phase = "silêncio" if elapsed < args.speak_after else "fala"
            if phase == "silêncio":
                silent_levels.append(level)
            else:
                speech_levels.append(level)

            relation = "<" if level < args.threshold else ">="
            print(
                f"t={elapsed:5.2f}s phase={phase:8s} level={level:.5f} {relation} threshold={args.threshold:.5f} peak={peak:.5f}"
            )

    print()
    print("=== resumo ===")
    print(f"geral:     {format_stats(all_levels)}")
    print(f"silêncio:  {format_stats(silent_levels)}")
    print(f"fala:      {format_stats(speech_levels)}")

    if silent_levels:
        print(f"média silêncio: {mean(silent_levels):.5f}")
    if speech_levels:
        print(f"média fala:     {mean(speech_levels):.5f}")

    if silent_levels and speech_levels:
        silent_avg = mean(silent_levels)
        speech_avg = mean(speech_levels)
        ratio = speech_avg / silent_avg if silent_avg > 0 else float("inf")
        print(f"relação fala/silêncio: {ratio:.2f}x")

    print("=== fim ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
