from __future__ import annotations

from app.config import APP_NAME, WAKE_WORD, OLLAMA_MODEL
from app.dialog.manager import DialogueManager
from app.state_machine import RobotState


class KidRoboCLI:
    def __init__(self) -> None:
        self.state = RobotState.STANDBY
        self.dialog = DialogueManager()

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
                print("KidRobo: Oi! Estou ouvindo! Pode falar.")
                self.state = RobotState.LISTENING

            elif self.state == RobotState.LISTENING:
                user_text = input("[criança] > ").strip()
                if not user_text:
                    self.state = RobotState.STANDBY
                else:
                    self.pending_text = user_text
                    self.state = RobotState.TRANSCRIBING

            elif self.state == RobotState.TRANSCRIBING:
                print(f"[transcrevendo] Texto reconhecido: {self.pending_text}")
                self.state = RobotState.THINKING

            elif self.state == RobotState.THINKING:
                response = self.dialog.reply(self.pending_text)
                self.pending_response = response
                self.state = RobotState.SPEAKING

            elif self.state == RobotState.SPEAKING:
                print(f"KidRobo: {self.pending_response}\n")
                self.state = RobotState.STANDBY

            elif self.state == RobotState.ERROR:
                print("KidRobo: Tive um probleminha. Vamos tentar de novo.")
                self.state = RobotState.STANDBY


def main() -> None:
    app = KidRoboCLI()
    app.run()


if __name__ == "__main__":
    main()
