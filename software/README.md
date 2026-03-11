# Software do KidRobo

A aplicação principal do Raspberry Pi ficará nesta pasta.

## Objetivos da primeira versão
- máquina de estados funcional
- fluxo completo de standby → escuta → STT → resposta → TTS
- suporte a respostas locais e fallback via Ollama
- módulos desacoplados para facilitar testes

## Estrutura prevista
- `app/main.py` ponto de entrada
- `app/state_machine.py` máquina de estados
- `app/audio/` entrada e saída de áudio
- `app/stt/` engine de transcrição
- `app/tts/` engine de fala
- `app/dialog/` intenções, respostas, segurança e integração Ollama
- `app/hardware/` LEDs, botões e ponte serial

## Teste inicial por CLI
No ambiente virtual:

```bash
python -m app.main
```

Fluxo do teste:
1. digitar `kidrobo`
2. fazer uma pergunta
3. verificar se a resposta veio por regra local ou via Ollama
