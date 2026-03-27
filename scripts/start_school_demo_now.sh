#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${KIDROBO_INSTALL_DIR:-$HOME/KidRobo}"
VENV_DIR="$INSTALL_DIR/.venv"

echo "[KidRobo] preparando microfone para a demo escolar..."
amixer -c 3 sset 'Mic' 12%
amixer -c 3 sset 'Auto Gain Control' off

echo "[KidRobo] entrando no ambiente virtual..."
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

cd "$INSTALL_DIR/software"

echo "[KidRobo] iniciando school-demo-fluid em modo terminal..."
echo "[KidRobo] use Ctrl+C para encerrar."
exec python -m app.main --mode school-demo-fluid --no-display
