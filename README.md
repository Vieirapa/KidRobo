# KidRobo

Protótipo educacional com Raspberry Pi para demonstrar para crianças pequenas como robôs podem ouvir, falar e interagir de forma lúdica e segura.

## Objetivo
Construir um MVP baseado em Raspberry Pi capaz de:
- ficar em espera por uma palavra de ativação
- ouvir perguntas simples
- responder com voz amigável
- usar sinais visuais simples (LEDs)
- evoluir depois para brincadeiras, sensores e movimento

## Princípios do projeto
- foco em latência baixa
- comportamento previsível
- linguagem simples para crianças
- priorização de componentes e ferramentas open source
- arquitetura modular para facilitar testes no Raspberry Pi

## Estrutura inicial
- `docs/` documentação funcional e técnica
- `software/` código da aplicação do Raspberry Pi
- `hardware/` documentação de hardware e integrações futuras com Arduino
- `assets/` imagens, diagramas e recursos multimídia
- `experiments/` protótipos e testes rápidos
- `scripts/` instalação, diagnóstico e execução na Raspberry Pi

## Funcionalidades já presentes
- simulador CLI
- respostas híbridas: regras locais + Ollama
- STT com `faster-whisper`
- TTS com `espeak-ng`
- modo demo
- scripts de diagnóstico e teste de áudio
- instalador inicial para Raspberry Pi
- instalador de serviço `systemd` em modo demo

## Roadmap resumido
1. Documentação e arquitetura inicial
2. MVP com wake word + STT + resposta guiada/LLM + TTS
3. Teste em Raspberry Pi
4. LEDs, botão físico e pequenas expressões
5. Integração opcional com Arduino
6. Brincadeiras e interações guiadas

## Stack inicial sugerida
- Raspberry Pi 4 ou 5
- Python 3.11+
- faster-whisper
- Ollama com `qwen2.5:0.5b`
- espeak-ng para TTS inicial
- gpiozero
- systemd para execução automática em demo

## Instalação na Raspberry Pi
Veja `docs/raspberry-install.md`.

## Status
Em desenvolvimento inicial com simulador CLI, STT/TTS básicos, integração com Ollama, modo demo e automação inicial de instalação.
