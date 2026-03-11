#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${KIDROBO_INSTALL_DIR:-$HOME/KidRobo}"
VENV_DIR="$INSTALL_DIR/.venv"
AUDIO_TEST_FILE="${KIDROBO_AUDIO_TEST_FILE:-/tmp/kidrobo_manual_test.wav}"

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

cd "$INSTALL_DIR/software"
python - <<PY
from app.audio.input import AudioInput
from app.stt import FasterWhisperEngine

output = "$AUDIO_TEST_FILE"
audio = AudioInput()
stt = FasterWhisperEngine()
print("[KidRobo] gravando áudio...")
path = audio.record_until_silence(output)
print(f"[KidRobo] arquivo salvo em: {path}")
text = stt.transcribe_file(path)
print(f"[KidRobo] texto reconhecido: {text}")
PY
