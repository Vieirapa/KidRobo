# Instalação do KidRobo na Raspberry Pi

## Objetivo
Permitir instalar o projeto a partir do GitHub com o menor número possível de passos manuais.

## Pré-requisitos
- Raspberry Pi OS com acesso à internet
- acesso SSH à Raspberry Pi
- chave SSH configurada para acessar o repositório privado no GitHub

## Instalação recomendada
Entrar na Raspberry Pi via SSH e executar:

```bash
git clone git@github.com:Vieirapa/KidRobo.git
cd KidRobo
chmod +x scripts/install_kidrobo_rpi.sh scripts/run_kidrobo.sh scripts/bootstrap_from_github.sh
./scripts/install_kidrobo_rpi.sh git@github.com:Vieirapa/KidRobo.git
```

## O que o script faz
- instala dependências de sistema
- clona ou atualiza o repositório
- cria ambiente virtual Python
- instala dependências Python
- instala o Ollama, se necessário
- baixa o modelo `qwen2.5:0.5b`

## Executando o KidRobo
```bash
./scripts/run_kidrobo.sh
```

## Observações
- o script atual prepara a base do sistema, mas ainda não configura serviço `systemd` do KidRobo
- o TTS inicial usa `espeak-ng`
- o STT usa `faster-whisper` com modelo `tiny`
- conforme o projeto crescer, o script poderá instalar novos componentes automaticamente
