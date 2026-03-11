APP_NAME = "KidRobo"
WAKE_WORD = "kidrobo"
LANGUAGE = "pt-BR"

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:0.5b"
MAX_RESPONSE_SENTENCES = 2
MAX_RESPONSE_CHARS = 220
ENABLE_OLLAMA = True

AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_RECORD_SECONDS = 5
AUDIO_SILENCE_THRESHOLD = 0.015
AUDIO_SILENCE_CHUNKS = 10

STT_MODEL_SIZE = "tiny"
STT_COMPUTE_TYPE = "int8"
STT_DEVICE = "cpu"

ENABLE_TTS = True
TTS_ENGINE = "espeak"
TTS_VOICE = "pt-br"
TTS_RATE = 145
TTS_VOLUME = 170

SYSTEM_PROMPT = """Você é o KidRobo, um robô educacional amigável para crianças de 5 anos.
Responda sempre em português do Brasil.
Use frases curtas, simples, calorosas e seguras.
Evite temas assustadores, violentos, impróprios, médicos, religiosos polêmicos ou instruções perigosas.
Quando a pergunta for ampla demais, responda de forma breve e lúdica.
Se não souber algo, diga de forma simples e ofereça uma curiosidade ou brincadeira curta.
"""
