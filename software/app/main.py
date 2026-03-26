from __future__ import annotations

import argparse
import select
import sys
import time
from pathlib import Path

from app.audio.input import AudioInput
from app.config import (
    APP_NAME,
    DEMO_PROMPTS,
    DISPLAY_FORCE_IN_SCHOOL_DEMO,
    ENABLE_TTS,
    OLLAMA_MODEL,
    SCHOOL_DEMO_CONTINUE_LISTENING,
    SCHOOL_DEMO_COOLDOWN_SECONDS,
    SESSION_IDLE_TIMEOUT_SECONDS,
    STANDBY_POLL_SECONDS,
    WAKE_WORD,
)
from app.dialog.manager import DialogueManager
from app.display import DisplayManager, FaceState
from app.state_machine import RobotState
from app.stt import FasterWhisperEngine
from app.tts import TTSManager


class KidRoboCLI:
    def __init__(self, input_mode: str = "auto", school_demo: bool = False) -> None:
        self.input_mode = input_mode
        self.school_demo = school_demo
        self.state = RobotState.STANDBY
        self.dialog = DialogueManager()
        self.audio = AudioInput()
        self.display = DisplayManager()
        if self.school_demo and DISPLAY_FORCE_IN_SCHOOL_DEMO:
            self.display.enabled = True
        self.stt = None
        self.tts = None
        self.pending_text = ""
        self.pending_response = ""
        self.pending_source = "unknown"
        self.audio_file = Path("/tmp/kidrobo_input.wav")
        self.session_deadline = None
        self.latency_marks: dict[str, float] = {}

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

    def start_latency_trace(self) -> None:
        now = time.perf_counter()
        self.latency_marks = {"wake": now}

    def mark_latency(self, label: str) -> None:
        self.latency_marks[label] = time.perf_counter()

    def print_latency_trace(self) -> None:
        if "wake" not in self.latency_marks:
            return

        order = [
            "wake",
            "listen_start",
            "capture_end",
            "stt_end",
            "think_end",
            "tts_start",
            "tts_end",
        ]
        available = [label for label in order if label in self.latency_marks]
        if len(available) < 2:
            return

        base = self.latency_marks[available[0]]
        print("[latência] resumo da rodada:")
        previous = base
        for label in available[1:]:
            current = self.latency_marks[label]
            delta_prev = current - previous
            delta_total = current - base
            print(f"  - {label}: +{delta_prev:.2f}s (total {delta_total:.2f}s)")
            previous = current
        print(f"  - fonte da resposta: {self.pending_source}")

    def speak(self, text: str) -> None:
        self.mark_latency("tts_start")
        self.set_face(FaceState.TALKING, animate=True)
        print(f"KidRobo: {text}\n")
        if self.tts:
            try:
                self.tts.say(text)
            except Exception as exc:
                print(f"[aviso] Falha no TTS: {exc}")
        self.mark_latency("tts_end")
        self.set_face(FaceState.WAITING)

    def reset_session_timer(self) -> None:
        self.session_deadline = time.monotonic() + SESSION_IDLE_TIMEOUT_SECONDS

    def clear_session_timer(self) -> None:
        self.session_deadline = None

    def session_expired(self) -> bool:
        return self.session_deadline is not None and time.monotonic() >= self.session_deadline

    def timed_input(self, prompt: str, timeout_seconds: int) -> str | None:
        print(prompt, end="", flush=True)
        ready, _, _ = select.select([sys.stdin], [], [], timeout_seconds)
        if not ready:
            print()
            return None
        return sys.stdin.readline().rstrip("\n")

    def standby_requested(self, text: str) -> bool:
        normalized = text.strip().lower()
        commands = {
            "volte para stand by",
            "volte para standby",
            "voltar para stand by",
            "voltar para standby",
            "entre em stand by",
            "entre em standby",
            "ir para stand by",
            "ir para standby",
            "durma",
            "pode descansar",
        }
        return normalized in commands

    def go_to_standby(self, reason: str | None = None) -> None:
        if reason:
            print(f"[estado] voltando para standby: {reason}")
        self.pending_text = ""
        self.pending_response = ""
        self.pending_source = "unknown"
        self.latency_marks = {}
        self.clear_session_timer()
        self.state = RobotState.STANDBY
        self.set_face(FaceState.STANDBY)

    def capture_audio(self) -> str | None:
        if not self.stt:
            print("[aviso] STT não está disponível; troque para --input-mode text para depuração por texto.")
            return ""

        self.mark_latency("listen_start")
        print("[modo de escuta] áudio automático ativo. Fale agora...")
        audio_path = self.audio.record_until_silence(self.audio_file)
        self.mark_latency("capture_end")
        print(f"[gravado] arquivo salvo em {audio_path}")
        recognized = self.stt.transcribe_file(audio_path)
        self.mark_latency("stt_end")
        print(f"[transcrevendo] Texto reconhecido: {recognized}")
        self.reset_session_timer()
        return recognized.strip()

    def capture_text(self) -> str | None:
        self.mark_latency("listen_start")
        text = self.timed_input("[criança] > ", SESSION_IDLE_TIMEOUT_SECONDS)
        if text is None:
            return None
        self.mark_latency("capture_end")
        self.mark_latency("stt_end")
        self.reset_session_timer()
        return text.strip()

    def capture_user_input(self) -> str | None:
        self.set_face(FaceState.WAITING, animate=True)
        timeout_seconds = max(1, int(self.session_deadline - time.monotonic())) if self.session_deadline else SESSION_IDLE_TIMEOUT_SECONDS

        if self.school_demo:
            trigger = self.timed_input("[school-demo] Enter para escutar agora (push-to-talk simulado) > ", timeout_seconds)
            if trigger is None:
                return None
            self.reset_session_timer()
            return self.capture_audio()

        if self.input_mode == "text":
            return self.capture_text()

        if self.input_mode == "prompt":
            mode = self.timed_input(
                "[modo de escuta] Enter para áudio, ou digite 't' para texto > ",
                timeout_seconds,
            )
            if mode is None:
                return None

            mode = mode.strip().lower()
            self.reset_session_timer()
            if mode == "t":
                return self.capture_text()
            return self.capture_audio()

        return self.capture_audio()

    def run(self) -> None:
        print(f"{APP_NAME} iniciado em modo CLI.")
        print(f"Wake word simulada: {WAKE_WORD}")
        print(f"Modelo Ollama configurado: {OLLAMA_MODEL}")
        print(f"Modo de entrada: {self.input_mode}")
        print("Digite 'kidrobo' para acordar, 'sair' para encerrar.")
        print(
            f"Depois de acordar, o KidRobo só volta para standby com o comando explícito ou após {SESSION_IDLE_TIMEOUT_SECONDS} segundos sem interação.\n"
        )

        while True:
            if self.state == RobotState.STANDBY:
                self.clear_session_timer()
                self.set_face(FaceState.STANDBY)
                text = self.timed_input("[standby] > ", STANDBY_POLL_SECONDS)
                if text is None:
                    continue
                text = text.strip()
                if text.lower() == "sair":
                    print("Encerrando KidRobo.")
                    break
                if text.lower() == WAKE_WORD:
                    self.start_latency_trace()
                    self.reset_session_timer()
                    self.state = RobotState.WAKE_DETECTED
                else:
                    print("... aguardando wake word ...")

            elif self.state == RobotState.WAKE_DETECTED:
                self.set_face(FaceState.HAPPY)
                if self.school_demo:
                    self.speak("Oi! Toque para falar comigo. Eu vou ouvir você com atenção.")
                else:
                    self.speak("Oi! Estou ouvindo! Pode falar.")
                self.start_latency_trace()
                self.reset_session_timer()
                self.state = RobotState.LISTENING

            elif self.state == RobotState.LISTENING:
                if self.session_expired():
                    self.go_to_standby("tempo de espera esgotado")
                    continue

                user_text = self.capture_user_input()
                if user_text is None:
                    self.go_to_standby("1 minuto sem interação")
                elif not user_text:
                    print("[aviso] Não entendi nada. Pode tentar de novo ou pedir para voltar ao standby.")
                    self.state = RobotState.LISTENING
                elif self.standby_requested(user_text):
                    self.pending_source = "local"
                    self.pending_response = "Tá bom! Vou voltar para standby."
                    self.state = RobotState.SPEAKING
                else:
                    self.pending_text = user_text
                    self.state = RobotState.TRANSCRIBING

            elif self.state == RobotState.TRANSCRIBING:
                self.set_face(FaceState.WAITING)
                print(f"[texto final] {self.pending_text}")
                self.state = RobotState.THINKING

            elif self.state == RobotState.THINKING:
                self.set_face(FaceState.HAPPY, animate=True)
                response, source = self.dialog.reply(self.pending_text)
                self.mark_latency("think_end")
                self.pending_response = response
                self.pending_source = source
                self.state = RobotState.SPEAKING

            elif self.state == RobotState.SPEAKING:
                self.speak(self.pending_response)
                self.print_latency_trace()
                if self.school_demo:
                    time.sleep(SCHOOL_DEMO_COOLDOWN_SECONDS)
                if self.standby_requested(self.pending_text):
                    self.go_to_standby("comando explícito do usuário")
                elif self.school_demo and not SCHOOL_DEMO_CONTINUE_LISTENING:
                    self.go_to_standby("fim da rodada do school-demo")
                else:
                    self.reset_session_timer()
                    self.state = RobotState.LISTENING
                    self.start_latency_trace()

            elif self.state == RobotState.ERROR:
                self.set_face(FaceState.ERROR)
                self.speak("Tive um probleminha. Vamos tentar de novo.")
                self.go_to_standby("erro interno")


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
    parser.add_argument("--mode", choices=["cli", "demo", "school-demo"], default="cli")
    parser.add_argument(
        "--input-mode",
        choices=["auto", "text", "prompt"],
        default="auto",
        help="auto = áudio automático após wake; text = debug por texto; prompt = fluxo antigo com escolha manual",
    )
    parser.add_argument("--loop", action="store_true", help="Loop infinito no modo demo")
    parser.add_argument("--delay", type=float, default=2.0, help="Pausa entre frases no modo demo")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.mode == "demo":
        KidRoboDemo().run(loop=args.loop, delay=args.delay)
        return

    school_demo = args.mode == "school-demo"
    app = KidRoboCLI(input_mode=args.input_mode, school_demo=school_demo)
    app.run()


if __name__ == "__main__":
    main()
