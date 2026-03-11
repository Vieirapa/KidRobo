# KidRobo v0.1 — Blueprint técnico completo

## 1. Visão geral
KidRobo é um protótipo educacional baseado em Raspberry Pi, pensado para demonstrar a crianças de aproximadamente 5 anos como um robô pode ouvir, falar e brincar com elas de forma simples, segura e previsível.

A proposta inicial é deliberadamente enxuta: capturar uma chamada, escutar uma pergunta, compreender o áudio, gerar uma resposta adequada e falar de volta com baixa latência.

---

## 2. Objetivo do MVP
Construir uma aplicação capaz de:
- permanecer em standby
- detectar uma palavra de ativação
- ouvir uma fala curta
- converter fala em texto
- gerar uma resposta simples e segura
- responder por voz
- retornar ao modo de espera

---

## 3. Arquitetura funcional recomendada
```text
[Microfone]
   ↓
[Wake Word Engine]
   ↓
[Captura de fala + VAD]
   ↓
[STT - Speech to Text]
   ↓
[Orquestrador de diálogo]
   ↓
[Motor de resposta]
   ├─ FAQ / regras
   ├─ brincadeiras guiadas
   └─ LLM opcional (futuro)
   ↓
[Filtro de segurança infantil]
   ↓
[TTS]
   ↓
[Alto-falante]
   ↓
[LEDs / efeitos / movimento opcional]
```

---

## 4. Estratégia recomendada
Para o KidRobo v0.1, o melhor caminho é **não usar LLM como cérebro principal**.

A recomendação é:
- wake word local
- STT local
- motor de intenções com regras simples
- TTS local
- LEDs / efeitos simples

### Por quê?
- menor latência
- mais previsível para crianças pequenas
- maior robustez offline
- depuração mais simples
- menor risco de respostas inadequadas

---

## 5. Hardware recomendado

### Mínimo viável
- Raspberry Pi 5
- fonte oficial
- microSD de qualidade ou SSD USB
- microfone USB
- alto-falante USB ou P2
- 1 LED RGB

### Configuração ideal para demo
- Raspberry Pi 5
- SSD USB
- microfone USB de boa captação
- speaker amplificado pequeno
- LED RGB ou pequeno display OLED
- botão físico de mute
- botão físico push-to-talk (opcional)
- case amigável para apresentação

### Papel do Arduino
O Arduino não precisa entrar no MVP, mas faz sentido nas próximas fases para:
- LEDs mais elaborados
- servos
- buzzer
- sensores
- leitura de botões e periféricos simples

### Divisão sugerida
- **Raspberry Pi:** áudio, IA, diálogo, lógica principal
- **Arduino:** I/O físico, efeitos, sensores e movimento

---

## 6. Máquina de estados
Estados sugeridos:
- `STANDBY`
- `WAKE_DETECTED`
- `LISTENING`
- `TRANSCRIBING`
- `THINKING`
- `SPEAKING`
- `ERROR`

### Fluxo principal
```text
STANDBY
  ↓
ouviu “KidRobo”
  ↓
“Oi! Estou ouvindo!”
  ↓
LISTENING
  ↓
captura da fala
  ↓
TRANSCRIBING
  ↓
texto válido?
  ├─ não → resposta de fallback
  └─ sim → THINKING
                ↓
         geração de resposta
                ↓
             SPEAKING
                ↓
             STANDBY
```

---

## 7. Estados e responsabilidades

### STANDBY
- escuta wake word
- mantém LED em modo de espera
- consome pouca CPU quando possível

### WAKE_DETECTED
- toca beep curto
- altera LED para indicar escuta
- inicia janela de captura

### LISTENING
- grava fala da criança
- usa VAD para detectar fim da fala

### TRANSCRIBING
- converte áudio em texto
- avalia se há transcrição útil

### THINKING
- identifica intenção
- consulta resposta local
- aplica política infantil

### SPEAKING
- executa TTS
- reproduz áudio
- evita conflito de escuta durante reprodução

### ERROR
- executa fallback seguro
- tenta recuperar o fluxo normal

---

## 8. Módulos de software

### 8.1 Audio Input
Responsável por:
- captura de áudio
- interface com microfone
- buffers de entrada

### 8.2 Wake Word
Responsável por:
- detectar palavra-chave como “KidRobo”
- iniciar o fluxo de atendimento

### 8.3 VAD
Responsável por:
- detectar início e fim de fala
- evitar gravação longa demais

### 8.4 STT
Responsável por:
- converter fala em texto
- retornar texto normalizado

### 8.5 Dialogue Manager
Responsável por:
- classificar intenção
- escolher resposta
- manter contexto muito curto

### 8.6 Safety Layer
Responsável por:
- limitar conteúdo
- restringir tamanho da resposta
- substituir incerteza por respostas seguras

### 8.7 TTS
Responsável por:
- gerar voz amigável
- tocar resposta com latência baixa

### 8.8 Expression Layer
Responsável por:
- LEDs de status
- sons curtos
- display ou servo opcional

### 8.9 Hardware Bridge
Responsável por:
- GPIO local
- ou ponte serial com Arduino

---

## 9. Stack sugerida

### MVP preferido
- **Linguagem:** Python 3.11+
- **Wake word:** OpenWakeWord ou Porcupine
- **VAD:** Silero VAD ou WebRTC VAD
- **STT:** faster-whisper
- **TTS:** Piper
- **GPIO:** gpiozero
- **Logs:** logging nativo do Python
- **Serviço:** systemd

### Alternativa futura com LLM
- Ollama com modelo pequeno
- uso apenas como fallback controlado
- sempre após filtro e limites rígidos

---

## 10. Segurança infantil
Regras recomendadas:
- respostas curtas
- linguagem simples
- sem temas inadequados
- sem instruções perigosas
- sem excesso de improviso
- sem fingir autoridade emocional profunda
- fallback seguro quando não entender

### Exemplos de fallback
- “Não entendi muito bem. Pode repetir?”
- “Vamos tentar de novo, bem devagar?”
- “Posso responder perguntas simples ou brincar com você!”

---

## 11. Modos de interação sugeridos

### Conversa simples
- “Oi”
- “Qual seu nome?”
- “Você é um robô?”
- “Vamos brincar?”

### Brincadeiras guiadas
- contar até 10
- imitar sons de animais
- adivinhações simples
- repetir palavras

### Curiosidades curtas
- fatos curtos sobre espaço, animais e robôs

### Efeitos físicos
- mudar cor do LED
- emitir som divertido
- mexer pequeno servo (fase futura)

---

## 12. Estrutura sugerida de diretórios
```text
KidRobo/
├── README.md
├── docs/
│   ├── blueprint-kidrobo-v0.1.md
│   ├── architecture.md
│   └── implementation-plan.md
├── software/
│   ├── README.md
│   ├── app/
│   │   ├── main.py
│   │   ├── state_machine.py
│   │   ├── config.py
│   │   ├── audio/
│   │   ├── stt/
│   │   ├── tts/
│   │   ├── dialog/
│   │   └── hardware/
│   ├── tests/
│   └── requirements.txt
├── hardware/
│   ├── README.md
│   └── bill-of-materials.md
├── assets/
└── experiments/
```

---

## 13. Pseudofluxo principal
```python
while True:
    if state == STANDBY:
        if wakeword.detected():
            leds.wake()
            audio.play_beep()
            state = LISTENING

    elif state == LISTENING:
        speech = audio.capture_until_silence()
        if not speech:
            state = STANDBY
        else:
            state = TRANSCRIBING

    elif state == TRANSCRIBING:
        text = stt.transcribe(speech)
        if not text:
            response = "Não entendi muito bem. Pode repetir?"
            state = SPEAKING
        else:
            state = THINKING

    elif state == THINKING:
        response = dialog.generate_response(text)
        response = safety.filter(response)
        state = SPEAKING

    elif state == SPEAKING:
        tts.say(response)
        leds.idle()
        state = STANDBY
```

---

## 14. Indicadores visuais sugeridos
- verde = standby
- azul = ouvindo
- amarelo = processando
- roxo = falando
- vermelho = erro

---

## 15. Requisitos não funcionais

### Latência
Meta inicial:
- wake word quase instantâneo
- STT em 1–2 s
- decisão de resposta em < 500 ms com regras locais
- TTS com início rápido

### Robustez
- reinício automático via systemd
- logs locais
- tratamento explícito de erro
- watchdog simples no futuro

### Operação
- iniciar junto com o boot
- rodar sem interface gráfica
- poder ser testado por CLI inicialmente

---

## 16. Riscos técnicos
1. **Microfone ruim compromete tudo**
2. **LLM local no Pi pode ser lento**
3. **Eco de áudio pode atrapalhar STT**
4. **Respostas abertas demais aumentam risco infantil**

---

## 17. MVP recomendado
### Hardware
- Raspberry Pi 5
- microfone USB
- speaker
- LED RGB
- botão opcional

### Software
- wake word “KidRobo”
- STT com faster-whisper
- TTS com Piper
- motor local com intenções
- cerca de 20–30 respostas prontas
- 5 brincadeiras guiadas

### Capacidades
- cumprimentar
- responder nome
- responder “o que você faz?”
- contar curiosidade curta
- brincar de contar
- fazer sons divertidos

---

## 18. Evolução por fases
### Fase 1
MVP de voz com resposta guiada

### Fase 2
LEDs, botão, display/olhos, animações e brincadeiras melhores

### Fase 3
Integração opcional com Arduino

### Fase 4
LLM pequeno como fallback controlado

---

## 19. Recomendação final
Para o primeiro KidRobo, a arquitetura ideal é:
- pipeline local
- regras + intenções como núcleo
- LLM apenas depois e com controle rígido

Isso é mais adequado para um produto embarcado real, mais confiável para demonstração infantil e melhor alinhado com uma primeira validação no Raspberry Pi.
