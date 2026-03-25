# KidRobo — roteiro curto de teste em campo

## Objetivo
Validar rapidamente, antes da demo, se o KidRobo está pronto para interagir com crianças.

## Teste de 5 minutos

### Etapa 1 — inicialização
1. ligar Raspberry Pi
2. abrir KidRobo em `school-demo`
3. confirmar face de standby na tela

### Etapa 2 — áudio
1. acionar push-to-talk
2. falar perto do microfone: "Oi, KidRobo"
3. confirmar se houve transcrição inteligível
4. confirmar se a resposta saiu pelo speaker certo

### Etapa 3 — perguntas infantis
Fazer estas perguntas:
- qual é seu nome?
- quem fez você?
- você é meu amigo?
- você conhece a Maria Antonia?
- você sabe contar?

### Etapa 4 — robustez rápida
1. falar mais baixo
2. falar com um pouco de ruído ambiente
3. verificar se o robô continua entendível e previsível

### Etapa 5 — encerramento
1. verificar se o app continua estável após algumas rodadas
2. confirmar que dá para reiniciar rapidamente se necessário

## Resultado esperado
O KidRobo é considerado pronto se:
- responde rápido o suficiente
- fala de forma audível
- mostra a face correta
- não depende excessivamente do Ollama nas perguntas principais
- não entra em comportamento estranho após poucas interações
