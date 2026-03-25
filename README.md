# KidRobo

Protótipo educacional com Raspberry Pi para demonstrar para crianças pequenas como robôs podem ouvir, falar e interagir de forma lúdica, segura e com baixa latência.

> Repositório atual do projeto em evolução. Este README resume o que já foi implementado, o que foi validado até agora e o que ainda falta.

## Visão geral
O KidRobo é um robô educativo pensado para rodar em Raspberry Pi, com foco em:
- interação por voz
- respostas simples e seguras para crianças
- arquitetura modular e fácil de depurar
- priorização de ferramentas open source
- possibilidade de expressão visual por tela e, depois, periféricos físicos

A direção atual do projeto é **offline-first com comportamento previsível**, usando respostas locais/intents como primeira camada e **Ollama** como fallback para perguntas abertas.

## Objetivo do MVP
Construir uma base funcional capaz de:
- ficar em standby aguardando ativação
- ouvir a fala da criança
- transcrever o áudio localmente
- responder com voz amigável
- continuar ouvindo por uma janela curta, sem operador humano
- exibir estados visuais simples em tela

---

## Status atual do projeto
### O que já está implementado
- aplicação principal em **Python** com execução por CLI
- fluxo de estados básico do robô (`standby`, wake, listening, thinking, speaking, error)
- **STT local com `faster-whisper`**
- **TTS com `espeak-ng`**
- respostas híbridas:
  - intents e respostas locais para perguntas infantis comuns
  - fallback para **Ollama** em perguntas abertas
  - fallback local resiliente quando o Ollama falha ou demora
- modo padrão mais natural com **escuta automática por áudio após wake**
- modo de **debug por texto**
- modo legado com prompt manual para troubleshooting
- medição de **latência por etapa** da rodada
- continuidade de conversa após a resposta, com retorno ao standby apenas por:
  - comando explícito
  - timeout de inatividade
- preparação do sistema visual com **rosto por estados** usando imagens full-screen
- scripts de instalação, execução, diagnóstico e teste de áudio
- serviço `systemd` inicial para rodar em modo demo

### O que já foi decidido tecnicamente
- Raspberry Pi 4 é a referência prática inicial
- modelo LLM inicial definido: **`qwen2.5:0.5b`** via Ollama
- `qwen2.5:0.5b` foi mantido por ser a melhor escolha prática atual para uso contínuo no Raspberry Pi 4
- STT inicial: `faster-whisper`
- TTS inicial: `espeak-ng`
- abordagem de diálogo: **respostas locais primeiro, LLM depois**
- entrada por texto permanece apenas como ferramenta de debug, não como fluxo principal

### O que já foi validado / atacado
- mudança do modo padrão para **áudio automático** após wake
- preservação de modos auxiliares para depuração
- ampliação das intents locais para perguntas infantis simples
- instrumentação de latência no fluxo principal
- correção do comportamento para **não derrubar o app** quando o Ollama falha/timeout
- adaptação da captura para **sample rate suportado** pelo hardware real quando 16 kHz não está disponível
- fallback prático quando `webrtcvad` não está disponível no ambiente atual

### O que ainda precisa de validação em campo
- ajuste fino de ganho/ruído do microfone USB na Raspberry Pi real
- thresholds de captura e silêncio em ambiente real de uso
- redução de autocaptura da própria fala do robô
- testes curtos com criança/ambiente real para validar timing de turn-taking

---

## Principais funcionalidades presentes hoje
### 1. Fluxo principal de conversa
Depois de acordar com `kidrobo`, o sistema:
1. entra em estado de escuta
2. captura áudio automaticamente
3. transcreve com STT local
4. classifica a pergunta
5. responde por regras locais ou Ollama
6. fala a resposta
7. continua ouvindo por uma janela de sessão

Isso já deixa o projeto bem mais próximo de uma interação real do que o fluxo antigo dependente de ENTER.

### 2. Modos disponíveis
#### Modo padrão mais próximo do uso real
```bash
cd software
python -m app.main
```

#### Debug por texto
```bash
cd software
python -m app.main --input-mode text
```

#### Fluxo legado com escolha manual
```bash
cd software
python -m app.main --input-mode prompt
```

#### Modo demo
```bash
cd software
python -m app.main --mode demo
```

### 3. Respostas locais já implementadas
O sistema já possui intents e respostas locais para temas infantis comuns, como:
- saudação
- nome
- idade
- propósito do robô
- brincadeira
- piada
- dinossauros
- espaço
- animais
- cor favorita
- curiosidades
- contagem
- perguntas sobre robôs

Quando a pergunta não cai bem nas intents locais, o sistema tenta Ollama. Se Ollama falhar, o KidRobo volta para um fallback seguro.

### 4. Sistema visual de rosto
O projeto já está preparado para usar imagens **800 x 480** em tela cheia, organizadas por estado:
- `standby`
- `happy`
- `talking`
- `angry`
- `afraid`
- `waiting`
- `error`

Veja também:
- `docs/display-face-system.md`
- `assets/faces/README.md`

---

## Estrutura do repositório
- `docs/` documentação funcional e técnica
- `software/` código da aplicação principal
- `hardware/` notas e documentação de hardware
- `scripts/` instalação, execução, diagnóstico e utilitários
- `assets/` recursos visuais e mídias do personagem
- `experiments/` testes rápidos e protótipos

---

## Stack atual
- **Raspberry Pi 4 ou 5**
- **Python 3.11+**
- **faster-whisper** para STT
- **Ollama** com `qwen2.5:0.5b`
- **espeak-ng** para TTS inicial
- **feh** / **fbi** para renderização full-screen de imagens
- **systemd** para automação de execução

## Trade-offs atuais
### Pontos fortes
- forte uso de componentes open source
- arquitetura simples de depurar
- comportamento mais previsível que depender 100% de LLM
- custo computacional mais compatível com Raspberry Pi

### Limitações atuais
- wake word ainda está em fase simulada / preparatória
- TTS inicial prioriza robustez, não naturalidade máxima
- qualidade da experiência ainda depende do hardware de áudio real
- há trabalho pendente para evitar autocaptura e melhorar turn-taking

### Dependência proprietária
Neste estágio, a base principal do projeto continua em ferramentas open source. Se no futuro entrar voz premium, STT premium, serviços cloud ou assets proprietários, isso deve ser documentado explicitamente com riscos e trade-offs.

---

## Instalação na Raspberry Pi
Veja a documentação principal em:
- `docs/raspberry-install.md`

Fluxo típico:
```bash
git clone git@github.com:Vieirapa/KidRobo.git
cd KidRobo
chmod +x scripts/*.sh
./scripts/install_kidrobo_rpi.sh git@github.com:Vieirapa/KidRobo.git
```

## Diagnóstico e testes
### Diagnóstico geral
```bash
./scripts/diagnose_kidrobo.sh
```

### Teste de áudio / STT
```bash
./scripts/test_audio.sh
```

---

## Documentação importante
### Visão técnica
- `docs/architecture.md`
- `docs/mvp-modules.md`
- `docs/ollama-strategy.md`

### Planejamento e status
- `docs/current-status.md`
- `docs/implementation-plan.md`
- `docs/blueprint-kidrobo-v0.1.md`

### Raspberry / operação
- `docs/raspberry-install.md`
- `docs/systemd-service.md`

### Display / rosto
- `docs/display-face-system.md`

---

## Status resumido por frente
### Aplicação principal
- [x] base funcional em Python
- [x] state machine principal
- [x] integração inicial de STT
- [x] integração inicial de TTS
- [x] fallback local + Ollama
- [x] latência instrumentada
- [ ] ajuste fino de interação no hardware real

### Experiência de voz
- [x] entrada automática por áudio após wake
- [x] modo texto para debug
- [x] conversa contínua com timeout de sessão
- [ ] calibrar ruído, silêncio e ganho
- [ ] reduzir autocaptura
- [ ] validar melhor experiência em campo

### Visual / expressão
- [x] estrutura por estados visuais
- [x] renderização preparada com `feh`/`fbi`
- [ ] popular assets finais de rosto
- [ ] sincronizar melhor imagem e fala

### Operação na Raspberry Pi
- [x] script de instalação
- [x] script de execução
- [x] script de diagnóstico
- [x] serviço `systemd` inicial em demo
- [ ] operação contínua validada em uso prolongado

---

## Próximos passos recomendados
1. estabilizar a captura de áudio real na Raspberry Pi
2. calibrar thresholds e reduzir ruído do microfone USB
3. melhorar o turn-taking para evitar atropelos
4. validar conversa contínua em cenário real
5. amadurecer o rosto visual com assets definitivos
6. evoluir para wake word real quando a base de áudio estiver estável
7. depois disso, integrar LEDs, botão físico e periféricos adicionais

---

## Resumo executivo
Hoje o KidRobo **já é um protótipo funcional de conversa por voz** com:
- STT local
- TTS local
- respostas locais + fallback via Ollama
- fluxo de conversa mais natural
- base visual para rosto em tela
- scripts de instalação e operação

O maior trabalho pendente não é mais “começar o projeto”, e sim **lapidar o comportamento real no Raspberry Pi**, principalmente na parte de áudio, ruído, timing e robustez da conversa.
