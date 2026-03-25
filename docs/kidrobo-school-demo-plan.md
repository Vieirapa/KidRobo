# KidRobo — Plano técnico executável para a demo escolar

## Contexto
Este plano é focado na apresentação do **Dia das Profissões** para crianças pequenas (~5 anos), usando o KidRobo como robô interativo em Raspberry Pi.

## Objetivo real da demo
Entregar uma experiência:
- simpática
- previsível
- segura
- rápida
- visualmente clara
- robusta o suficiente para ambiente escolar

O objetivo **não** é demonstrar um assistente universal. O objetivo é fazer a criança sentir que está falando com um robô vivo e amigável.

## Critério de sucesso
A demo é considerada bem-sucedida se a maioria das crianças perceber:
- que o robô ouviu
- que o robô respondeu
- que ele "tem carinha"
- que ele parece interagir de verdade
- que foi construído de forma compreensível e encantadora

## Estratégia de UX para demo
### Fluxo recomendado
1. KidRobo fica em standby com face visível na tela.
2. A criança **toca na tela** ou aciona **push-to-talk**.
3. O robô entra claramente em estado de escuta.
4. A criança fala.
5. O sistema responde com frase curta e segura.
6. O robô volta para standby ou permanece por uma janela curta de continuação.

### Decisão importante
Para a demo escolar, o fluxo principal deve ser:
- **touch-to-talk / push-to-talk**, não wake word real.

Justificativa:
- mais confiável em ambiente com ruído
- reduz atrito para crianças pequenas
- diminui falhas de timing
- facilita demonstração pública

## Escopo da primeira entrega da demo
### Entram nesta etapa
- modo `school-demo`
- display ativo por padrão nesse modo
- push-to-talk / touch-to-talk
- expansão de intents infantis
- cooldown pós-fala para reduzir autocaptura
- documento passo a passo para instalação no Raspberry Pi

### Ficam fora desta etapa
- wake word robusta final
- integração com Arduino
- LEDs avançados
- animação facial complexa em tempo real
- voz premium
- grandes mudanças arquiteturais

## Backlog priorizado

### Prioridade 1 — demo confiável
1. Criar `school-demo mode`
2. Implementar fluxo de push-to-talk / touch-to-talk
3. Ativar display no modo demo escolar
4. Adicionar cooldown pós-TTS
5. Expandir intents locais infantis
6. Revisar concisão e simpatia das respostas locais infantis

### Prioridade 2 — demo encantadora
7. Melhorar assets faciais e coerência visual
8. Ajustar tempo de troca de estados visuais
9. Adicionar feedback visual claro de escuta e pensamento
10. Ajustar resposta para ainda mais concisão e simpatia

### Prioridade 3 — operação em Raspberry
11. Criar documento passo a passo de instalação e operação
12. Revisar scripts de instalação/diagnóstico
13. Criar checklist de validação pré-demo
14. Definir roteiro curto de teste em campo

## Riscos principais e mitigação

### Risco: a criança falar e o robô não entender
Mitigação:
- push-to-talk
- instrução simples na tela
- testes de ganho e microfone antes da demo

### Risco: o robô se ouvir e responder à própria voz
Mitigação:
- cooldown pós-fala
- ajuste físico de speaker/microfone
- thresholds melhores

### Risco: resposta inadequada ou estranha
Mitigação:
- mais intents locais
- safety mais dura
- fallback curto e seguro
- reduzir dependência do Ollama na demo

### Risco: latência parecer ruim
Mitigação:
- feedback visual explícito de estados
- respostas curtas
- preferir respostas locais

## Entregáveis desta fase
1. Documento de plano técnico da demo escolar
2. Implementação inicial do `school-demo mode`
3. Base do fluxo de `push-to-talk`
4. Documento passo a passo de instalação e operação no Raspberry Pi

## Próximo movimento após este documento
1. Implementar `school-demo mode`
2. Implementar push-to-talk
3. Ativar display no modo demo
4. Ajustar safety e intents
5. Escrever e revisar documentação Raspberry
