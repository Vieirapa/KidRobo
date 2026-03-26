# KidRobo — voz e frases do school-demo

## Voz atual
Configuração atual do TTS para o school-demo:
- engine: `espeak-ng`
- voz: `pt-br+f4`
- taxa: `140`

Objetivo:
- manter caráter de robô
- melhorar compreensão em português do Brasil
- reduzir a sensação de fala acelerada

## Frases de wake
As frases de entrada do school-demo ficam em:
- `software/app/dialog/school_demo_prompts.py`

Essas frases são curtas e variam a cada rodada para evitar repetição cansativa.

## Frases de idle
O mesmo arquivo também guarda frases de "matar o tempo" em standby.

### Intenção
Dar ao KidRobo um pouco mais de presença em ambiente de apresentação.

### Regras atuais
- só no `school-demo`
- em intervalos aleatórios entre 10 e 40 segundos
- devem soar simpáticas, leves e convidativas
- não devem soar carentes, agressivas ou assustadoras

## Evolução futura
Depois da apresentação, podemos:
- aumentar bastante a biblioteca de frases
- separar por contexto (escola, robôs, engenharia, brincadeira)
- adicionar diversidade por energia/humor do personagem
