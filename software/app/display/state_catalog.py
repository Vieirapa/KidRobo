from __future__ import annotations

from enum import Enum


class FaceState(str, Enum):
    STANDBY = "standby"
    HAPPY = "happy"
    TALKING = "talking"
    ANGRY = "angry"
    AFRAID = "afraid"
    WAITING = "waiting"
    ERROR = "error"


STATE_DIR_MAP = {
    FaceState.STANDBY: "standby",
    FaceState.HAPPY: "happy",
    FaceState.TALKING: "talking",
    FaceState.ANGRY: "angry",
    FaceState.AFRAID: "afraid",
    FaceState.WAITING: "waiting",
    FaceState.ERROR: "error",
}
