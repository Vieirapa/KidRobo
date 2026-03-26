from __future__ import annotations

import random

SCHOOL_DEMO_WAKE_LINES = [
    "Oi! Toque aí para falar comigo.",
    "Estou pronto! Toque para eu te ouvir.",
    "Vamos conversar? Toque na tela.",
    "Pode me chamar! Toque para falar.",
    "Oi! Quer bater um papo comigo?",
    "Toque aqui e fale comigo.",
    "Estou ouvindo! Toque para começar.",
    "Vamos brincar? Toque para falar.",
    "Pode falar comigo! Toque aí.",
    "Estou pronto para conversar.",
]

SCHOOL_DEMO_IDLE_LINES = [
    "Nossa, quanta gente!",
    "Que escola legal. Posso vir para aula todo dia?",
    "Ei, vocês parecem estar gostando. Toca na tela para falar comigo!",
    "Estou aqui esperando um papo bem legal.",
    "Se alguém quiser conversar, é só tocar na tela.",
    "Eu adoro robôs, escola e perguntas curiosas.",
    "Será que alguém vai me perguntar meu nome?",
    "Posso contar uma curiosidade se você tocar na tela.",
    "Estou pronto para uma conversa de robô.",
    "Tem alguém aí querendo brincar comigo?",
]


def random_school_demo_wake_line() -> str:
    return random.choice(SCHOOL_DEMO_WAKE_LINES)


def random_school_demo_idle_line() -> str:
    return random.choice(SCHOOL_DEMO_IDLE_LINES)


def random_idle_interval_seconds() -> float:
    return random.uniform(10.0, 40.0)
