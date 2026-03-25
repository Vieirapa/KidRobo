from __future__ import annotations

import time
from pathlib import Path

from app.config import DISPLAY_ASSETS_DIR, DISPLAY_ENABLED, DISPLAY_FRAME_DELAY_SECONDS
from app.display.face_assets import FaceAssetRepository
from app.display.renderer import FaceRenderer
from app.display.state_catalog import FaceState


class DisplayManager:
    def __init__(self, assets_dir: str | Path = DISPLAY_ASSETS_DIR) -> None:
        self.enabled = DISPLAY_ENABLED
        self.assets = FaceAssetRepository(assets_dir)
        self.renderer = FaceRenderer()
        self.current_state = FaceState.STANDBY

    def set_state(self, state: FaceState, render: bool = True) -> None:
        self.current_state = state
        if render:
            self.render_once(state)

    def render_once(self, state: FaceState | None = None) -> Path | None:
        target_state = state or self.current_state
        frame = self.assets.next_frame(target_state)
        if not frame:
            return None
        if self.enabled and self.renderer.available():
            self.renderer.show_image(frame)
        return frame

    def animate_state(self, state: FaceState, cycles: int = 3) -> list[Path]:
        rendered: list[Path] = []
        for _ in range(cycles):
            frame = self.render_once(state)
            if frame:
                rendered.append(frame)
            time.sleep(DISPLAY_FRAME_DELAY_SECONDS)
        return rendered
