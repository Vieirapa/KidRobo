from pathlib import Path

APP_NAME = "KidRobo"
WAKE_WORD = "kidrobo"
LANGUAGE = "pt-BR"

APP_DIR = Path(__file__).resolve().parent
SOFTWARE_DIR = APP_DIR.parent
PROJECT_ROOT = SOFTWARE_DIR.parent

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:0.5b"
MAX_RESPONSE_SENTENCES = 2
MAX_RESPONSE_CHARS = 220
ENABLE_OLLAMA = True
SESSION_IDLE_TIMEOUT_SECONDS = 60
SCHOOL_DEMO_COOLDOWN_SECONDS = 1.0
SCHOOL_DEMO_CONTINUE_LISTENING = False

AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_RECORD_SECONDS = 10
AUDIO_SILENCE_THRESHOLD = 0.015
AUDIO_SILENCE_CHUNKS = 10
AUDIO_TEST_FILE = "/tmp/kidrobo_test.wav"
AUDIO_USE_VAD = True
AUDIO_VAD_MODE = 2
AUDIO_VAD_FRAME_MS = 30
AUDIO_VAD_START_FRAMES = 3
AUDIO_VAD_END_FRAMES = 20
AUDIO_VAD_PREROLL_FRAMES = 10

STT_MODEL_SIZE = "tiny"
STT_COMPUTE_TYPE = "int8"
STT_DEVICE = "cpu"

ENABLE_TTS = True
TTS_ENGINE = "espeak"
TTS_VOICE = "pt-br"
TTS_RATE = 145
TTS_VOLUME = 170

DISPLAY_ENABLED = False
DISPLAY_FORCE_IN_SCHOOL_DEMO = True
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480
DISPLAY_ASSETS_DIR = str(PROJECT_ROOT / "assets" / "faces")
DISPLAY_FRAME_DELAY_SECONDS = 0.6

DEMO_PROMPTS = [
    "Oi! Eu sou o KidRobo. Quer conversar comigo?",
    "Você pode me perguntar meu nome ou pedir uma curiosidade.",
    "Eu adoro aprender com crianças curiosas.",
]

SYSTEM_PROMPT = """Você é o KidRobo, um robô educacional amigável para crianças de 5 anos.
Responda sempre em português do Brasil.
Use frases curtas, simples, calorosas e seguras.
Evite temas assustadores, violentos, impróprios, médicos, religiosos polêmicos ou instruções perigosas.
Quando a pergunta for ampla demais, responda de forma breve e lúdica.
Se não souber algo, diga de forma simples e ofereça uma curiosidade ou brincadeira curta.
"""
