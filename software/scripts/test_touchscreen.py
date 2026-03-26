#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from app.hardware.touch import TouchConfig, TouchInput


def main() -> int:
    parser = argparse.ArgumentParser(description="Teste simples do touchscreen do KidRobo")
    parser.add_argument("--device", default="", help="Caminho do device de input (ex: /dev/input/event9)")
    parser.add_argument("--seconds", type=float, default=15.0, help="Tempo máximo de espera por toque")
    parser.add_argument("--debounce", type=float, default=0.35, help="Debounce entre toques")
    args = parser.parse_args()

    touch = None
    if args.device:
        touch = TouchInput(TouchConfig(device_path=args.device, debounce_seconds=args.debounce))
        touch.open()
    else:
        touch = TouchInput.autodetect(debounce_seconds=args.debounce)

    if not touch:
        print("[touch-test] nenhum touchscreen detectado")
        return 1

    print(f"[touch-test] usando dispositivo: {touch.device_path}")
    print(f"[touch-test] toque na tela nos próximos {args.seconds:.1f}s...")

    deadline = time.monotonic() + args.seconds
    touches = 0
    while time.monotonic() < deadline:
        if touch.wait_for_touch(0.5):
            touches += 1
            print(f"[touch-test] toque detectado #{touches}")

    print(f"[touch-test] fim do teste; total de toques detectados: {touches}")
    return 0 if touches > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
