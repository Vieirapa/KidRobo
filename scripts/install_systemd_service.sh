#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${KIDROBO_INSTALL_DIR:-$HOME/KidRobo}"
SERVICE_NAME="kidrobo.service"
SYSTEMD_DIR="$HOME/.config/systemd/user"
SERVICE_PATH="$SYSTEMD_DIR/$SERVICE_NAME"

mkdir -p "$SYSTEMD_DIR"

cat > "$SERVICE_PATH" <<SERVICE
[Unit]
Description=KidRobo School Demo Service
After=network-online.target sound.target graphical-session.target
Wants=network-online.target

[Service]
Type=simple
Environment=KIDROBO_INSTALL_DIR=$INSTALL_DIR
WorkingDirectory=$INSTALL_DIR/software
ExecStartPre=/bin/sleep 1
ExecStartPre=/usr/bin/amixer -c 3 sset Mic 12%
ExecStartPre=/usr/bin/amixer -c 3 sset 'Auto Gain Control' off
ExecStart=$INSTALL_DIR/scripts/run_kidrobo.sh --mode school-demo-fluid --no-display
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
