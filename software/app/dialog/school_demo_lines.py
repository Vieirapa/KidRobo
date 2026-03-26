from __future__ import annotations

import random
from typing import Sequence

SCHOOL_DEMO_FALLBACK_LINES = [
    "Ops, minhas anteninhas não pegaram isso direitinho. Posso falar sobre robôs ou contar uma curiosidade.",
    "Ih, embaralhou um pouquinho aqui nos meus circuitos. Quer perguntar meu nome ou pedir uma curiosidade?",
    "Hehe, essa parte escapou das minhas engrenagens. Posso brincar, contar ou falar sobre robôs.",
    "Não peguei tudinho, mas continuo fofinho e prestando atenção. Quer uma curiosidade bem legal?",
    "Posso conversar com você! Tente me perguntar meu nome ou peça uma curiosidade de robô.",
    "Se quiser, eu posso falar sobre engenharia, robôs ou alguma coisa curiosa.",
    "Minhas orelhas de robô ficaram meio confusas. Quer que eu conte uma curiosidade sobre como robôs funcionam?",
    "Bip bip... acho que perdi um pedacinho da pergunta. Mas ainda posso te contar algo legal.",
    "A pergunta deu uma cambalhota dentro de mim. Vamos tentar de novo?",
    "Hum... meu cérebro de parafusos não entendeu tudo. Quer falar mais devagar ou pedir uma curiosidade?",
]


def _random_line(lines: Sequence[str], last_line: str | None = None) -> str:
    if not lines:
        return ""
    if len(lines) == 1:
        return lines[0]

    choices = [line for line in lines if line != last_line]
    if not choices:
        choices = list(lines)
    return random.choice(choices)


def random_school_demo_fallback(last_line: str | None = None) -> str:
    return _random_line(SCHOOL_DEMO_FALLBACK_LINES, last_line=last_line)
