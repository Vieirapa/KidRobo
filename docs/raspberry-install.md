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
chmod +x scripts/*.sh
./scripts/install_kidrobo_rpi.sh git@github.com:Vieirapa/KidRobo.git
```

## O que o script faz
- instala dependências de sistema
- instala ferramentas de display (`feh` e `fbi`)
- clona ou atualiza o repositório
- cria ambiente virtual Python
- instala dependências Python
- instala o Ollama, se necessário
- baixa o modelo `qwen2.5:0.5b`
- ajusta permissões dos scripts auxiliares

## Diagnóstico após instalação
```bash
./scripts/diagnose_kidrobo.sh
```

## Teste de áudio e STT
```bash
./scripts/test_audio.sh
```

## Executando o KidRobo
### modo CLI
```bash
./scripts/run_kidrobo.sh
```

### modo demo
```bash
./scripts/run_kidrobo.sh --mode demo
```

### modo demo em loop
```bash
./scripts/run_kidrobo.sh --mode demo --loop
```

## Sistema de rosto em tela
- coloque as imagens em `assets/faces/<estado>/`
- resolução recomendada: **800 x 480**
- veja `assets/faces/README.md`
- veja `docs/display-face-system.md`

## Instalar serviço systemd do usuário
```bash
./scripts/install_systemd_service.sh
systemctl --user start kidrobo.service
journalctl --user -u kidrobo.service -f
```

## Observações
- o serviço `systemd` criado roda o KidRobo em modo demo contínuo
- o TTS inicial usa `espeak-ng`
- o STT usa `faster-whisper` com modelo `tiny`
- o sistema já está preparado para estados visuais baseados em imagens full-screen
- conforme o projeto crescer, os scripts poderão instalar novos componentes automaticamente
