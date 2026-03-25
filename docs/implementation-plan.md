# Plano de implementação — KidRobo v0.2

## Objetivo desta etapa
Transformar o KidRobo de um simulador CLI assistido para uma experiência de conversa infantil mais natural no Raspberry Pi, com foco em:
- menor latência percebida e real
- menos pontos de erro na interação
- transição gradual do modo debug para o modo de uso real

---

## Estratégia geral
A implementação será dividida em **3 sprints curtos**, cada um com entregas funcionais e testáveis em Raspberry Pi.

### Princípio central
O fluxo principal deve ser:
- acordar
- ouvir automaticamente
- responder rápido
- continuar escutando por uma janela curta
- voltar para standby sem operador humano

Texto via terminal continuará existindo, mas apenas como ferramenta de debug.

---

# Sprint 1 — UX básica realista
## Objetivo
Eliminar o passo manual de escolher áudio por ENTER e aproximar o fluxo da experiência real da criança.

## Problemas atacados
- a criança não entende o timing do terminal
- a necessidade de apertar ENTER adiciona erro operacional
- o fluxo atual parece teste técnico, não conversa natural

## Entregas
- modo padrão com **áudio automático** após wake word simulada
- modo texto preservado apenas para debug
- modo legado com prompt manual preservado para comparação
- logs mais claros de modo de entrada e transições
- documentação atualizada do novo comportamento

## Critério de pronto
- após `kidrobo`, o sistema entra em escuta sem pedir ENTER
- ainda é possível depurar por texto com opção explícita
- fluxo continua estável no CLI

## Status
- [x] adicionar `--input-mode auto|text|prompt`
- [x] tornar `auto` o comportamento padrão
- [x] manter modo legado para troubleshooting
- [ ] validar no Raspberry Pi real

---

# Sprint 2 — Latência e percepção de resposta
## Objetivo
Reduzir o tempo entre a fala da criança e a reação do KidRobo, melhorando também a sensação de responsividade.

## Problemas atacados
- resposta parece lenta mesmo quando o sistema está funcionando
- parte do atraso vem da espera silenciosa sem feedback
- perguntas simples talvez estejam indo longe demais até o Ollama

## Entregas
- medição de latência por etapa:
  - início da escuta
  - fim da captura
  - fim da transcrição
  - fim da geração da resposta
  - início/fim do TTS
- revisão dos parâmetros de captura e silêncio
- criação explícita de estado/feedback de "pensando"
- expansão das respostas/intents locais para reduzir chamadas ao Ollama
- revisão do script de diagnóstico para refletir o modelo atual `qwen2.5:0.5b`

## Critério de pronto
- logs mostram onde a latência acontece
- perguntas comuns de criança resolvem localmente com mais frequência
- a experiência parece mais rápida, mesmo sem mudar toda a arquitetura

## Status
- [x] instrumentar latência no `main.py`
- [ ] revisar thresholds de áudio
- [x] expandir intents e respostas locais
- [x] alinhar diagnóstico com `qwen2.5:0.5b`
- [ ] validar ganho prático no Raspberry

---

# Sprint 3 — Conversa contínua robusta
## Objetivo
Permitir uma troca mais natural, reduzindo atropelos entre fala da criança e resposta do KidRobo.

## Problemas atacados
- a criança pode começar a falar por cima do robô
- o fluxo ainda é rígido demais entre speaking e listening
- falta uma janela de continuação mais natural

## Entregas
- janela curta de continuação após cada resposta
- timeout curto pós-resposta + timeout maior de sessão
- política básica para evitar recaptura indevida da própria voz do KidRobo
- testes práticos de turn-taking em Raspberry Pi
- preparação da base para wake word real depois

## Critério de pronto
- a conversa pode emendar naturalmente após uma resposta
- menos erros de timing por parte da criança
- o comportamento do robô fica mais previsível em uso real

## Status
- [ ] definir timeouts curto/longo
- [ ] ajustar transição `SPEAKING -> LISTENING`
- [ ] reduzir risco de autocaptura
- [ ] validar em teste de campo curto

---

## Ordem de execução recomendada
1. Sprint 1 — remover atrito humano do fluxo
2. Sprint 2 — atacar latência real e percebida
3. Sprint 3 — melhorar turn-taking e conversa contínua

---

## Registro de início imediato
Em 2026-03-24, o trabalho foi iniciado pelo **Sprint 1**, com a mudança do modo padrão para captura automática de áudio após wake e preservação do texto apenas como ferramenta explícita de debug.

## Registro adicional do Sprint 2
Em 2026-03-24, o Sprint 2 avançou com:
- instrumentação inicial de latência por rodada
- indicação da fonte da resposta (`local`, `ollama` ou `fallback`)
- expansão das intents locais para perguntas infantis comuns
- alinhamento do script de diagnóstico com o modelo `qwen2.5:0.5b`
