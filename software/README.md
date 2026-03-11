# Software do KidRobo

A aplicação principal do Raspberry Pi ficará nesta pasta.

## Objetivos da primeira versão
- máquina de estados funcional
- fluxo completo de standby → escuta → STT → resposta → TTS
- módulos desacoplados para facilitar testes

## Estrutura prevista
- `app/main.py` ponto de entrada
- `app/state_machine.py` máquina de estados
- `app/audio/` entrada e saída de áudio
- `app/stt/` engine de transcrição
- `app/tts/` engine de fala
- `app/dialog/` intenções, respostas e segurança
- `app/hardware/` LEDs, botões e ponte serial
