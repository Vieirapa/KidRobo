#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${1:-git@github.com:Vieirapa/KidRobo.git}"
TARGET_DIR="${2:-$HOME/KidRobo-bootstrap}"

mkdir -p "$TARGET_DIR"
if [ ! -d "$TARGET_DIR/.git" ]; then
  git clone "$REPO_URL" "$TARGET_DIR"
else
  git -C "$TARGET_DIR" pull --ff-only
fi

exec "$TARGET_DIR/scripts/install_kidrobo_rpi.sh" "$REPO_URL"
