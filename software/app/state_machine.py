from enum import Enum

class RobotState(str, Enum):
    STANDBY = "standby"
    WAKE_DETECTED = "wake_detected"
    LISTENING = "listening"
    TRANSCRIBING = "transcribing"
    THINKING = "thinking"
    SPEAKING = "speaking"
    ERROR = "error"
