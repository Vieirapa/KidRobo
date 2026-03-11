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
- integrar STT real
- integrar TTS real
- criar scripts de teste de áudio e diagnóstico

## Etapa 4 — Operação embarcada inicial
- criar modo demo
- criar scripts de instalação na Raspberry Pi
- instalar serviço `systemd` do usuário
- validar execução automática

## Etapa 5 — Wake word real
- integrar wake word
- reduzir falso positivo
- ajustar experiência de ativação

## Etapa 6 — Resposta híbrida
- manter intents básicas locais
- usar Ollama para respostas abertas curtas
- aplicar filtro infantil sempre

## Etapa 7 — Expressão física
- LED RGB para status
- botão opcional
- logs de transição de estado

## Etapa 8 — Primeiro teste de campo
- testar com perguntas simples
- medir tempo de resposta
- ajustar volume, microfone e ruído ambiente

## Critério de pronto do primeiro teste
- diagnóstico funcional
- transcrição aceitável
- resposta híbrida estável
- TTS inteligível
- demo operacional
- loop completo sem travamentos
