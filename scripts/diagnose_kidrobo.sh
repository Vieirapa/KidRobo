#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${KIDROBO_INSTALL_DIR:-$HOME/KidRobo}"
VENV_DIR="$INSTALL_DIR/.venv"
MODEL="${KIDROBO_OLLAMA_MODEL:-qwen2.5:0.5b}"

section() {
  printf '\n=== %s ===\n' "$1"
}

check_cmd() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "[ok] comando disponível: $1"
  else
    echo "[erro] comando ausente: $1"
  fi
}

section "Comandos básicos"
check_cmd python3
check_cmd git
check_cmd ollama
check_cmd espeak-ng
check_cmd ffmpeg

section "Ambiente virtual"
if [ -d "$VENV_DIR" ]; then
  echo "[ok] venv encontrado em $VENV_DIR"
else
  echo "[erro] venv não encontrado em $VENV_DIR"
fi

section "Dependências Python"
if [ -d "$VENV_DIR" ]; then
  # shellcheck disable=SC1090
  source "$VENV_DIR/bin/activate"
  python - <<'PY'
mods = ["numpy", "sounddevice", "faster_whisper", "av", "requests"]
for mod in mods:
    try:
        __import__(mod)
        print(f"[ok] módulo Python disponível: {mod}")
    except Exception as exc:
        print(f"[erro] módulo Python indisponível: {mod} -> {exc}")

try:
    import webrtcvad  # type: ignore
    print("[ok] módulo Python disponível: webrtcvad")
except Exception as exc:
    print(f"[aviso] webrtcvad indisponível neste ambiente: {exc}")
PY
fi

section "Ollama"
if command -v ollama >/dev/null 2>&1; then
  if ollama list | grep -q "$MODEL"; then
    echo "[ok] modelo presente: $MODEL"
  else
    echo "[erro] modelo ausente: $MODEL"
  fi
fi

section "Áudio (aplay/arecord)"
if command -v arecord >/dev/null 2>&1; then
  arecord -l || true
else
  echo "[aviso] arecord não disponível"
fi
if command -v aplay >/dev/null 2>&1; then
  aplay -l || true
else
  echo "[aviso] aplay não disponível"
fi

section "Fim do diagnóstico"
