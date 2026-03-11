from app.config import APP_NAME
from app.state_machine import RobotState


def main() -> None:
    state = RobotState.STANDBY
    print(f"{APP_NAME} iniciado. Estado atual: {state.value}")
    print("Protótipo inicial: a implementação dos módulos virá nas próximas etapas.")


if __name__ == "__main__":
    main()
