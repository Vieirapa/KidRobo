from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class FaceRenderer:
    def __init__(self) -> None:
        self.fbi = shutil.which("fbi")
        self.feh = shutil.which("feh")

    def available(self) -> bool:
        return bool(self.fbi or self.feh)

    def show_image(self, image_path: str | Path) -> None:
        image = str(image_path)

        if self.fbi:
            subprocess.run(
                [self.fbi, "-T", "1", "-d", "/dev/fb0", "--noverbose", "-a", image],
                check=True,
            )
            return

        if self.feh:
            subprocess.run([self.feh, "-F", image], check=True)
            return

        raise RuntimeError("Nenhum renderizador de imagem disponível (fbi/feh).")
