# KidRobo — teste focado em transições de estado

## Objetivo
Validar se o KidRobo muda visualmente entre os estados principais de uma rodada real de interação.

## Estados que queremos observar
- `standby`
- `happy` (wake detectado)
- `waiting` (escuta / preparação)
- `talking`
- `error` (se houver falha)

## Teste manual sugerido
Na Raspberry:

> Durante esta fase de teste de transições, priorize um modo de exibição que não roube o foco do terminal. Fullscreen agressivo pode atrapalhar o input enquanto ainda dependemos do terminal para o `school-demo`.


```bash
cd ~/KidRobo
source .venv/bin/activate
cd software
python -m app.main --mode school-demo
```

## Passo a passo de observação

### Etapa 1 — standby
- confirmar que a face de standby aparece corretamente na tela

### Etapa 2 — wake
No terminal, digitar:

```text
kidrobo
```

Observar:
- a face muda de `standby` para `happy`?
- o robô fala a frase de entrada?

### Etapa 3 — escuta
Depois do wake, observar:
- a face entra em `waiting`?
- o sistema parece pronto para ouvir?

### Etapa 4 — resposta
Falar uma pergunta simples, por exemplo:
- "qual é seu nome?"
- "quem fez você?"
- "você é meu amigo?"

Observar:
- a face muda para `talking` enquanto responde?
- o áudio sai corretamente?
- depois da resposta ele volta para `standby` no school-demo?

## Critério de sucesso
Considerar suficiente para a demo se:
- `standby`, `happy`, `waiting` e `talking` forem perceptíveis
- o áudio acompanhar a troca principal de estados
- o school-demo completar uma rodada sem travar

## Observações importantes
- Não bloquear a demo por falta de animação contínua em `standby`
- Priorizar mudança clara entre estados em vez de animação idle perfeita
