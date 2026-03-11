#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${1:-git@github.com:Vieirapa/KidRobo.git}"
INSTALL_DIR="${KIDROBO_INSTALL_DIR:-$HOME/KidRobo}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="$INSTALL_DIR/.venv"
MODEL="${KIDROBO_OLLAMA_MODEL:-qwen2.5:0.5b}"

log() {
  printf '\n[%s] %s\n' "KidRobo" "$1"
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Comando obrigatório não encontrado: $1" >&2
    exit 1
  }
}

log "Validando pré-requisitos básicos"
require_command git
require_command curl
require_command "$PYTHON_BIN"

log "Instalando dependências de sistema"
sudo apt-get update
sudo apt-get install -y \
  git \
  curl \
  ffmpeg \
  espeak-ng \
  portaudio19-dev \
  python3-venv \
  python3-dev \
  build-essential

if [ ! -d "$INSTALL_DIR/.git" ]; then
  log "Clonando repositório $REPO_URL em $INSTALL_DIR"
  git clone "$REPO_URL" "$INSTALL_DIR"
else
  log "Repositório já existe; atualizando"
  git -C "$INSTALL_DIR" pull --ff-only
fi

log "Criando ambiente virtual Python"
"$PYTHON_BIN" -m venv "$VENV_DIR"
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

log "Atualizando pip e instalando dependências Python"
pip install --upgrade pip wheel setuptools
pip install -r "$INSTALL_DIR/software/requirements.txt"

if ! command -v ollama >/dev/null 2>&1; then
  log "Instalando Ollama"
  curl -fsSL https://ollama.com/install.sh | sh
else
  log "Ollama já está instalado"
fi

log "Iniciando serviço Ollama"
if command -v systemctl >/dev/null 2>&1; then
  sudo systemctl enable ollama || true
  sudo systemctl start ollama || true
fi

log "Baixando modelo do Ollama: $MODEL"
ollama pull "$MODEL"

log "Instalação concluída"
echo "Repositório: $INSTALL_DIR"
echo "Ative o ambiente: source $VENV_DIR/bin/activate"
echo "Execute o KidRobo: cd $INSTALL_DIR/software && python -m app.main"
