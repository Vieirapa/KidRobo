# Arquitetura do KidRobo

## Visão em camadas

```text
┌──────────────────────────────────────────────┐
│                Interface Física              │
│  microfone, speaker, LEDs, botão, display   │
└──────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────┐
│                 Camada de Áudio              │
│    wake word, captura, VAD, playback         │
└──────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────┐
│              Camada de Processamento         │
│         STT, normalização, classificação     │
└──────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────┐
│             Camada de Orquestração           │
│     state machine, diálogo, segurança        │
└──────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────┐
│              Camada de Resposta              │
│      respostas locais, jogos, TTS            │
└──────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────┐
│            Camada de Ação / Expressão        │
│       voz, LEDs, serial com Arduino          │
└──────────────────────────────────────────────┘
```

## Princípios de arquitetura
- offline-first no MVP
- módulos trocáveis
- baixa latência
- previsibilidade para ambiente infantil
- fácil depuração em Linux embarcado

## Contratos entre módulos
- `wakeword` dispara evento `wake_detected`
- `audio` entrega buffer de fala
- `stt` entrega texto normalizado
- `dialog` retorna intenção e resposta
- `safety` filtra e aprova texto final
- `tts` sintetiza e reproduz
- `hardware` atualiza LEDs/efeitos

## Estratégia de evolução
1. simular tudo por CLI
2. integrar dispositivos reais no Raspberry Pi
3. adicionar LEDs e botões
4. conectar Arduino se houver periféricos de tempo real
5. adicionar fallback de LLM apenas depois do MVP estável
