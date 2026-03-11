from __future__ import annotations

import argparse
import time
from pathlib import Path

from app.audio.input import AudioInput
from app.config import APP_NAME, DEMO_PROMPTS, ENABLE_TTS, OLLAMA_MODEL, WAKE_WORD
from app.dialog.manager import DialogueManager
from app.display import DisplayManager, FaceState
from app.state_machine import RobotState
from app.stt import FasterWhisperEngine
from app.tts import TTSManager


class KidRoboCLI:
    def __init__(self) -> None:
        self.state = RobotState.STANDBY
        self.dialog = DialogueManager()
        self.audio = AudioInput()
        self.display = DisplayManager()
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

        self.display.set_state(FaceState.STANDBY, render=False)

    def set_face(self, state: FaceState, animate: bool = False) -> None:
        self.display.set_state(state, render=not animate)
        if animate:
            frames = self.display.animate_state(state)
            if frames:
                print(f"[display] {state.value}: {frames[-1]}")
            else:
                print(f"[display] sem imagens para o estado: {state.value}")
        else:
            frame = self.display.render_once(state)
            if frame:
                print(f"[display] {state.value}: {frame}")

    def speak(self, text: str) -> None:
        self.set_face(FaceState.TALKING, animate=True)
        print(f"KidRobo: {text}\n")
        if self.tts:
            try:
                self.tts.say(text)
            except Exception as exc:
                print(f"[aviso] Falha no TTS: {exc}")
        self.set_face(FaceState.WAITING)

    def capture_text(self) -> str:
        self.set_face(FaceState.WAITING, animate=True)
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
                self.set_face(FaceState.STANDBY, animate=True)
                text = input("[standby] > ").strip()
                if text.lower() == "sair":
                    print("Encerrando KidRobo.")
                    break
                if text.lower() == WAKE_WORD:
                    self.state = RobotState.WAKE_DETECTED
                else:
                    print("... aguardando wake word ...")

            elif self.state == RobotState.WAKE_DETECTED:
                self.set_face(FaceState.HAPPY)
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
                self.set_face(FaceState.WAITING)
                print(f"[texto final] {self.pending_text}")
                self.state = RobotState.THINKING

            elif self.state == RobotState.THINKING:
                self.set_face(FaceState.WAITING, animate=True)
                response = self.dialog.reply(self.pending_text)
                self.pending_response = response
                self.state = RobotState.SPEAKING

            elif self.state == RobotState.SPEAKING:
                self.speak(self.pending_response)
                self.state = RobotState.STANDBY

            elif self.state == RobotState.ERROR:
                self.set_face(FaceState.ERROR)
                self.speak("Tive um probleminha. Vamos tentar de novo.")
                self.state = RobotState.STANDBY


class KidRoboDemo:
    def __init__(self) -> None:
        self.display = DisplayManager()
        self.tts = None
        if ENABLE_TTS:
            try:
                self.tts = TTSManager()
            except Exception as exc:
                print(f"[aviso] TTS indisponível no demo: {exc}")

    def run(self, loop: bool = False, delay: float = 2.0) -> None:
        print(f"{APP_NAME} iniciado em modo demo.")
        while True:
            self.display.animate_state(FaceState.STANDBY)
            for phrase in DEMO_PROMPTS:
                self.display.set_state(FaceState.HAPPY)
                print(f"KidRobo: {phrase}")
                self.display.animate_state(FaceState.TALKING, cycles=4)
                if self.tts:
                    try:
                        self.tts.say(phrase)
                    except Exception as exc:
                        print(f"[aviso] Falha no TTS: {exc}")
                self.display.set_state(FaceState.WAITING)
                time.sleep(delay)
            if not loop:
                break


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KidRobo")
    parser.add_argument("--mode", choices=["cli", "demo"], default="cli")
    parser.add_argument("--loop", action="store_true", help="Loop infinito no modo demo")
    parser.add_argument("--delay", type=float, default=2.0, help="Pausa entre frases no modo demo")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.mode == "demo":
        KidRoboDemo().run(loop=args.loop, delay=args.delay)
        return

    app = KidRoboCLI()
    app.run()


if __name__ == "__main__":
    main()
