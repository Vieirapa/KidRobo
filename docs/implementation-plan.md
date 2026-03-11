# Plano de implementação — KidRobo v0.1

## Etapa 1 — Fundação do projeto
- definir estrutura do repositório
- documentar arquitetura
- preparar ambiente Python
- definir contratos entre módulos

## Etapa 2 — Simulador local com Ollama
- criar máquina de estados
- criar motor de intenções simples
- integrar Ollama como fallback para perguntas abertas
- simular eventos por texto no terminal
- validar fluxo completo sem hardware real

## Etapa 3 — Áudio no Raspberry Pi
- integrar captura de microfone
- integrar wake word
- integrar VAD
- reproduzir beep e resposta TTS

## Etapa 4 — STT real
- integrar faster-whisper
- medir latência
- ajustar tempo máximo de captura

## Etapa 5 — Resposta híbrida
- manter intents básicas locais
- usar Ollama para respostas abertas curtas
- aplicar filtro infantil sempre

## Etapa 6 — Expressão física
- LED RGB para status
- botão opcional
- logs de transição de estado

## Etapa 7 — Primeiro teste de campo
- testar com perguntas simples
- medir tempo de resposta
- ajustar volume, microfone e ruído ambiente

## Critério de pronto do primeiro teste
- wake word funcional
- transcrição aceitável
- resposta híbrida estável
- TTS inteligível
- loop completo sem travamentos
