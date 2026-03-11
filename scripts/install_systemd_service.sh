#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${KIDROBO_INSTALL_DIR:-$HOME/KidRobo}"
SERVICE_NAME="kidrobo.service"
SYSTEMD_DIR="$HOME/.config/systemd/user"
SERVICE_PATH="$SYSTEMD_DIR/$SERVICE_NAME"

mkdir -p "$SYSTEMD_DIR"

cat > "$SERVICE_PATH" <<SERVICE
[Unit]
Description=KidRobo Demo Service
After=network-online.target sound.target
Wants=network-online.target

[Service]
Type=simple
Environment=KIDROBO_INSTALL_DIR=$INSTALL_DIR
WorkingDirectory=$INSTALL_DIR/software
ExecStart=$INSTALL_DIR/scripts/run_kidrobo.sh --mode demo --loop
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
SERVICE

systemctl --user daemon-reload
systemctl --user enable "$SERVICE_NAME"

echo "Serviço instalado em: $SERVICE_PATH"
echo "Para iniciar agora: systemctl --user start $SERVICE_NAME"
echo "Para ver logs: journalctl --user -u $SERVICE_NAME -f"
