from __future__ import annotations

import random
from typing import Sequence

SCHOOL_DEMO_FALLBACK_LINES = {
    "confuso": [
        "Ops, minhas anteninhas não pegaram isso direitinho. Posso falar sobre robôs ou contar uma curiosidade.",
        "Ih, embaralhou um pouquinho aqui nos meus circuitos. Quer perguntar meu nome ou pedir uma curiosidade?",
        "Hehe, essa parte escapou das minhas engrenagens. Posso brincar, contar ou falar sobre robôs.",
        "Minhas orelhas de robô ficaram meio confusas. Quer que eu conte uma curiosidade sobre como robôs funcionam?",
        "Hum... meu cérebro de parafusos não entendeu tudo. Quer falar mais devagar ou pedir uma curiosidade?",
    ],
    "brincalhao": [
        "Não peguei tudinho, mas continuo fofinho e prestando atenção. Quer uma curiosidade bem legal?",
        "Bip bip... acho que perdi um pedacinho da pergunta. Mas ainda posso te contar algo legal.",
        "A pergunta deu uma cambalhota dentro de mim. Vamos tentar de novo?",
        "Acho que essa frase escorregou entre meus parafusos. Quer tentar mais uma vez?",
    ],
    "redirecionador": [
        "Posso conversar com você! Tente me perguntar meu nome ou peça uma curiosidade de robô.",
        "Se quiser, eu posso falar sobre engenharia, robôs ou alguma coisa curiosa.",
        "Quer me perguntar meu nome, pedir uma contagem ou ouvir uma curiosidade?",
    ],
}


def _flatten(groups: dict[str, list[str]]) -> list[str]:
    lines: list[str] = []
    for group_lines in groups.values():
        lines.extend(group_lines)
    return lines


def _random_line(lines: Sequence[str], recent_lines: Sequence[str] | None = None) -> str:
    if not lines:
        return ""
    if len(lines) == 1:
        return lines[0]

    recent = set(recent_lines or [])
    choices = [line for line in lines if line not in recent]
    if not choices:
        choices = list(lines)
    return random.choice(choices)


def _random_grouped_line(groups: dict[str, list[str]], recent_lines: Sequence[str] | None = None) -> str:
    recent = set(recent_lines or [])
    available_groups = [name for name, group_lines in groups.items() if any(line not in recent for line in group_lines)]
    group_name = random.choice(available_groups) if available_groups else random.choice(list(groups.keys()))
    return _random_line(groups[group_name], recent_lines=recent_lines)


def random_school_demo_fallback(recent_lines: Sequence[str] | None = None) -> str:
    return _random_grouped_line(SCHOOL_DEMO_FALLBACK_LINES, recent_lines=recent_lines)


def all_school_demo_fallback_lines() -> list[str]:
    return _flatten(SCHOOL_DEMO_FALLBACK_LINES)
