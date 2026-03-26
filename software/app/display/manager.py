from __future__ import annotations

import time
from pathlib import Path

from app.config import (
    DISPLAY_ANIMATE_CYCLES_HAPPY,
    DISPLAY_ANIMATE_CYCLES_STANDBY,
    DISPLAY_ANIMATE_CYCLES_TALKING,
    DISPLAY_ANIMATE_CYCLES_WAITING,
    DISPLAY_ASSETS_DIR,
    DISPLAY_ENABLED,
    DISPLAY_FRAME_DELAY_HAPPY_SECONDS,
    DISPLAY_FRAME_DELAY_SECONDS,
    DISPLAY_FRAME_DELAY_STANDBY_SECONDS,
    DISPLAY_FRAME_DELAY_TALKING_SECONDS,
    DISPLAY_FRAME_DELAY_WAITING_SECONDS,
)
from app.display.face_assets import FaceAssetRepository
from app.display.renderer import FaceRenderer
from app.display.state_catalog import FaceState


class DisplayManager:
    STATE_FRAME_DELAYS = {
        FaceState.STANDBY: DISPLAY_FRAME_DELAY_STANDBY_SECONDS,
        FaceState.WAITING: DISPLAY_FRAME_DELAY_WAITING_SECONDS,
        FaceState.TALKING: DISPLAY_FRAME_DELAY_TALKING_SECONDS,
        FaceState.HAPPY: DISPLAY_FRAME_DELAY_HAPPY_SECONDS,
    }

    STATE_ANIMATE_CYCLES = {
        FaceState.STANDBY: DISPLAY_ANIMATE_CYCLES_STANDBY,
        FaceState.WAITING: DISPLAY_ANIMATE_CYCLES_WAITING,
        FaceState.TALKING: DISPLAY_ANIMATE_CYCLES_TALKING,
        FaceState.HAPPY: DISPLAY_ANIMATE_CYCLES_HAPPY,
    }

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

    def animate_state(self, state: FaceState, cycles: int | None = None) -> list[Path]:
        rendered: list[Path] = []
        target_cycles = cycles if cycles is not None else self.STATE_ANIMATE_CYCLES.get(state, 3)
        frame_delay = self.STATE_FRAME_DELAYS.get(state, DISPLAY_FRAME_DELAY_SECONDS)
        for _ in range(target_cycles):
            frame = self.render_once(state)
            if frame:
                rendered.append(frame)
            time.sleep(frame_delay)
        return rendered
