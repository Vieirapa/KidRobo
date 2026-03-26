from __future__ import annotations

import random

SCHOOL_DEMO_FALLBACK_LINES = [
    "Não entendi direitinho, mas posso contar uma curiosidade sobre robôs.",
    "Acho que não ouvi tudo certinho. Quer que eu fale meu nome ou conte até dez?",
    "Hum, essa parte ficou confusa para mim. Posso brincar, contar ou falar sobre robôs.",
    "Não peguei direitinho a pergunta. Quer ouvir uma curiosidade bem legal?",
    "Posso conversar com você! Se quiser, pergunte meu nome ou peça uma curiosidade.",
]


def random_school_demo_fallback() -> str:
    return random.choice(SCHOOL_DEMO_FALLBACK_LINES)
