from __future__ import annotations

import random
from pathlib import Path

from app.display.state_catalog import FaceState, STATE_DIR_MAP


class FaceAssetRepository:
    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir)

    def list_frames(self, state: FaceState) -> list[Path]:
        state_dir = self.base_dir / STATE_DIR_MAP[state]
        if not state_dir.exists():
            return []

        frames = [
            path for path in sorted(state_dir.iterdir())
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        ]
        return frames

    def random_frame(self, state: FaceState) -> Path | None:
        frames = self.list_frames(state)
        if not frames:
            return None
        return random.choice(frames)
