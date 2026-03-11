#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${KIDROBO_INSTALL_DIR:-$HOME/KidRobo}"
VENV_DIR="$INSTALL_DIR/.venv"

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
cd "$INSTALL_DIR/software"
exec python -m app.main
