from __future__ import annotations

import os
import select
import struct
import time
from dataclasses import dataclass
from pathlib import Path

INPUT_EVENT_FORMAT = "llHHI"
INPUT_EVENT_SIZE = struct.calcsize(INPUT_EVENT_FORMAT)
EV_KEY = 0x01
BTN_TOUCH = 0x14A


@dataclass(slots=True)
class TouchConfig:
    device_path: str
    debounce_seconds: float = 0.35


class TouchInput:
    def __init__(self, config: TouchConfig) -> None:
        self.config = config
        self.device_path = Path(config.device_path)
        self.fd: int | None = None
        self.last_touch_at = 0.0

    @classmethod
    def autodetect(cls, debounce_seconds: float = 0.35) -> "TouchInput | None":
        candidates = cls._candidate_device_paths()
        for path in candidates:
            try:
                touch = cls(TouchConfig(device_path=str(path), debounce_seconds=debounce_seconds))
                touch.open()
                return touch
            except OSError:
                continue
        return None

    @staticmethod
    def _candidate_device_paths() -> list[Path]:
        paths: list[Path] = []
        by_id = Path("/dev/input/by-id")
        if by_id.exists():
            paths.extend(sorted(p.resolve() for p in by_id.glob("*event*") if "touch" in p.name.lower()))

        proc_devices = Path("/proc/bus/input/devices")
        if proc_devices.exists():
            blocks = proc_devices.read_text(encoding="utf-8", errors="ignore").split("\n\n")
            for block in blocks:
                low = block.lower()
                if "touch" not in low:
                    continue
                for line in block.splitlines():
                    if line.startswith("H: Handlers="):
                        for token in line.split()[2:]:
                            if token.startswith("event"):
                                paths.append(Path("/dev/input") / token)

        direct = Path("/dev/input")
        if direct.exists():
            paths.extend(sorted(direct.glob("event*")))

        seen: set[str] = set()
        unique: list[Path] = []
        for path in paths:
            key = str(path)
            if key in seen:
                continue
            seen.add(key)
            unique.append(path)
        return unique

    def open(self) -> None:
        if self.fd is not None:
            return
        self.fd = os.open(self.device_path, os.O_RDONLY | os.O_NONBLOCK)

    def close(self) -> None:
        if self.fd is None:
            return
        os.close(self.fd)
        self.fd = None

    def wait_for_touch(self, timeout_seconds: float) -> bool:
        if self.fd is None:
            self.open()

        ready, _, _ = select.select([self.fd], [], [], timeout_seconds)
        if not ready:
            return False

        detected = False
        while True:
            try:
                data = os.read(self.fd, INPUT_EVENT_SIZE)
            except BlockingIOError:
                break

            if len(data) < INPUT_EVENT_SIZE:
                break

            _, _, event_type, code, value = struct.unpack(INPUT_EVENT_FORMAT, data)
            if event_type == EV_KEY and code == BTN_TOUCH and value == 1:
                now = time.monotonic()
                if now - self.last_touch_at >= self.config.debounce_seconds:
                    self.last_touch_at = now
                    detected = True
        return detected
