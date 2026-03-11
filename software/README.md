# Software do KidRobo

A aplicação principal do Raspberry Pi fica nesta pasta.

## Objetivos da primeira versão
- máquina de estados funcional
- fluxo completo de standby → escuta → STT → resposta → TTS
- suporte a respostas locais e fallback via Ollama
- módulos desacoplados para facilitar testes

## Módulos já presentes
- `app/main.py` ponto de entrada e simulador CLI
- `app/state_machine.py` máquina de estados
- `app/audio/input.py` captura de áudio e gravação WAV
- `app/stt/faster_whisper_engine.py` transcrição com faster-whisper
- `app/tts/espeak_engine.py` síntese de voz inicial com espeak-ng
- `app/dialog/` intenções, respostas, segurança e integração Ollama

## Teste inicial por CLI
No ambiente virtual:

```bash
python -m app.main
```

Fluxo do teste:
1. digitar `kidrobo`
2. escolher `t` para texto ou `a` para áudio
3. fazer uma pergunta
4. verificar a resposta do KidRobo

## Observação sobre TTS
Neste momento o TTS inicial usa `espeak-ng` por simplicidade e robustez na Raspberry Pi.
No futuro podemos adicionar Piper como engine alternativa com voz mais natural.
