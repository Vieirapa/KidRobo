from __future__ import annotations

from pathlib import Path

from app.audio.input import AudioInput
from app.config import APP_NAME, ENABLE_TTS, OLLAMA_MODEL, WAKE_WORD
from app.dialog.manager import DialogueManager
from app.state_machine import RobotState
from app.stt import FasterWhisperEngine
from app.tts import TTSManager


class KidRoboCLI:
    def __init__(self) -> None:
        self.state = RobotState.STANDBY
        self.dialog = DialogueManager()
        self.audio = AudioInput()
        self.stt = None
        self.tts = None
        self.pending_text = ""
        self.pending_response = ""
        self.audio_file = Path("/tmp/kidrobo_input.wav")

        try:
            self.stt = FasterWhisperEngine()
        except Exception as exc:
            print(f"[aviso] STT indisponível no momento: {exc}")

        if ENABLE_TTS:
            try:
                self.tts = TTSManager()
            except Exception as exc:
                print(f"[aviso] TTS indisponível no momento: {exc}")

    def speak(self, text: str) -> None:
        print(f"KidRobo: {text}\n")
        if self.tts:
            try:
                self.tts.say(text)
            except Exception as exc:
                print(f"[aviso] Falha no TTS: {exc}")

    def capture_text(self) -> str:
        mode = input("[modo de escuta] digite 't' para texto ou 'a' para áudio > ").strip().lower()
        if mode == "a":
            if not self.stt:
                print("[aviso] STT não está disponível; usando entrada por texto.")
                return input("[criança] > ").strip()

            print("[gravando] fale agora...")
            audio_path = self.audio.record_until_silence(self.audio_file)
            print(f"[gravado] arquivo salvo em {audio_path}")
            recognized = self.stt.transcribe_file(audio_path)
            print(f"[transcrevendo] Texto reconhecido: {recognized}")
            return recognized

        return input("[criança] > ").strip()

    def run(self) -> None:
        print(f"{APP_NAME} iniciado em modo CLI.")
        print(f"Wake word simulada: {WAKE_WORD}")
        print(f"Modelo Ollama configurado: {OLLAMA_MODEL}")
        print("Digite 'kidrobo' para acordar, 'sair' para encerrar.\n")

        while True:
            if self.state == RobotState.STANDBY:
                text = input("[standby] > ").strip()
                if text.lower() == "sair":
                    print("Encerrando KidRobo.")
                    break
                if text.lower() == WAKE_WORD:
                    self.state = RobotState.WAKE_DETECTED
                else:
                    print("... aguardando wake word ...")

            elif self.state == RobotState.WAKE_DETECTED:
                self.speak("Oi! Estou ouvindo! Pode falar.")
                self.state = RobotState.LISTENING

            elif self.state == RobotState.LISTENING:
                user_text = self.capture_text()
                if not user_text:
                    self.state = RobotState.STANDBY
                else:
                    self.pending_text = user_text
                    self.state = RobotState.TRANSCRIBING

            elif self.state == RobotState.TRANSCRIBING:
                print(f"[texto final] {self.pending_text}")
                self.state = RobotState.THINKING

            elif self.state == RobotState.THINKING:
                response = self.dialog.reply(self.pending_text)
                self.pending_response = response
                self.state = RobotState.SPEAKING

            elif self.state == RobotState.SPEAKING:
                self.speak(self.pending_response)
                self.state = RobotState.STANDBY

            elif self.state == RobotState.ERROR:
                self.speak("Tive um probleminha. Vamos tentar de novo.")
                self.state = RobotState.STANDBY


def main() -> None:
    app = KidRoboCLI()
    app.run()


if __name__ == "__main__":
    main()
