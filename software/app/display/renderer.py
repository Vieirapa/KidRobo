from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image

from app.config import DISPLAY_ROTATE_DEGREES


class FaceRenderer:
    def __init__(self) -> None:
        self.fbi = shutil.which("fbi")
        self.feh = shutil.which("feh")
        self.tmp_dir = Path("/tmp/kidrobo-display")
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def available(self) -> bool:
        return bool(self.fbi or self.feh)

    def _prepare_image(self, image_path: str | Path) -> str:
        src = Path(image_path)
        if DISPLAY_ROTATE_DEGREES % 360 == 0:
            return str(src)

        dst = self.tmp_dir / f"rotated-{src.stem}.png"
        with Image.open(src) as img:
            rotated = img.rotate(-DISPLAY_ROTATE_DEGREES, expand=True)
            rotated.save(dst)
        return str(dst)

    def show_image(self, image_path: str | Path) -> None:
        image = self._prepare_image(image_path)

        if self.feh:
            subprocess.run(
                [self.feh, "-x", "-Y", "-Z", image],
                check=True,
            )
            return

        if self.fbi:
            subprocess.run(
                [self.fbi, "-T", "1", "-d", "/dev/fb0", "--noverbose", "-a", image],
                check=True,
            )
            return

        raise RuntimeError("Nenhum renderizador de imagem disponível (fbi/feh).")
