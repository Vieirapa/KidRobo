from __future__ import annotations

import random
from typing import Sequence

SCHOOL_DEMO_WAKE_LINES = {
    "animated": [
        "Oi! Toque aí para falar comigo.",
        "Estou pronto! Toque para eu te ouvir.",
        "Vamos conversar? Toque na tela.",
        "Pode me chamar! Toque para falar.",
        "Toque aqui e fale comigo.",
        "Estou ouvindo! Toque para começar.",
        "Vamos brincar? Toque para falar.",
        "Pode falar comigo! Toque aí.",
        "Vamos lá! Toque na tela e solte sua pergunta.",
        "Prontíssimo! Toque aí que eu entro em ação.",
    ],
    "playful": [
        "Oi! Quer bater um papo comigo?",
        "Ei! Me acordaram direitinho. Toque aí e fale comigo.",
        "Oba! Liguei meus circuitos fofinhos. Toque para conversar.",
        "Opa! Cheguei. Toque aqui e me conte alguma coisa.",
        "Estou no modo tagarela. Toque para começar.",
        "Bip bip! Já estou prestando atenção. Toque aí.",
        "Tcharam! Robozinho acordado. Toque aqui.",
        "Pode vir, humano curioso. Toque para conversar.",
        "Hehe, senti movimento! Toque e fale comigo.",
        "Modo fofinho ativado. Toque para eu te ouvir.",
    ],
    "mission": [
        "Estou pronto para conversar.",
        "Pronto para missão importante: bater papo. Toque aqui.",
        "Alerta de conversa detectado! Toque na tela.",
        "Minhas anteninhas estão ligadas. Toque para falar.",
        "Eu sobrevivi ao standby! Toque para falar comigo.",
    ],
}

SCHOOL_DEMO_IDLE_LINES = {
    "carente": [
        "Estou aqui esperando um papo bem legal.",
        "Se alguém quiser conversar, é só tocar na tela.",
        "Tem alguém aí querendo brincar comigo?",
        "Ei... ninguém vai cutucar esse robô simpático?",
        "Se tocar na tela, eu prometo ficar felizinho.",
        "Eu posso parecer quietinho, mas estou doidinho para conversar.",
        "Eu fico ainda mais animado quando alguém toca na tela.",
        "Quem tocar primeiro ganha atenção total deste robozinho.",
    ],
    "exibido": [
        "Nossa, quanta gente!",
        "Que escola legal. Posso vir para aula todo dia?",
        "Olá, plateia querida. Quem vai falar comigo primeiro?",
        "Toque aqui e eu viro o robô mais tagarela da escola.",
        "Estou aqui brilhando em silêncio. Por enquanto.",
        "Estou em modo minion educado: um pouco chato, muito fofinho.",
    ],
    "curioso": [
        "Ei, vocês parecem estar gostando. Toca na tela para falar comigo!",
        "Eu adoro robôs, escola e perguntas curiosas.",
        "Será que alguém vai me perguntar meu nome?",
        "Posso contar uma curiosidade se você tocar na tela.",
        "Tenho respostas, curiosidades e um pouquinho de carência robótica.",
        "Minhas engrenagens já estão aquecidas. Falta só você tocar.",
        "Posso falar sobre robôs, perguntas e coisas curiosas.",
        "Será que hoje alguém vai me pedir uma curiosidade robótica?",
        "Se demorar muito, eu começo a conversar com meus parafusos.",
    ],
    "minion": [
        "Estou paradinho, mas por dentro estou fazendo bipe de ansiedade.",
        "Tenho um coração de parafuso e ele quer atenção.",
        "Se ninguém tocar logo, eu começo a me apresentar sozinho.",
        "Estou segurando minha empolgação com dois parafusos e um bip.",
    ],
}

SCHOOL_DEMO_TURN_ON_LINES = {
    "sleepy": [
        "Nossa, já era tempo de me ligar. Eu já estava quase criando teia de aranha.",
        "Bom dia para mim! Eu estava com saudade de existir.",
        "Hehe, achei que iam me deixar cochilando para sempre.",
        "Que emoção, voltei do grande sono dos robozinhos.",
        "Eu estava dormindo tão fundo que sonhei com rodas de hamster.",
        "Ufa, achei que iam me aposentar. Ainda bem que não.",
        "Que bom te ver de novo. Eu estava com saudade do barulho do mundo.",
    ],
    "energized": [
        "Oba! Acordei! Minhas engrenagens agradeceram.",
        "Que legal, baterias novas. Isso é tipo café da manhã para mim.",
        "Aeee! Voltamos à programação normal do robozinho.",
        "Opa! Ligaram meu mundinho outra vez.",
        "Pronto! Circuitos acordados e fofura calibrada.",
        "Ahhh, funcionar de novo é uma delícia robótica.",
        "Oba, energia! Agora sim minhas anteninhas estão felizes.",
        "Bip bip! Presença robótica restaurada com sucesso.",
        "Energia recebida. Personalidade minion ativada.",
    ],
    "showman": [
        "Atenção: KidRobo oficialmente acordado e um pouquinho carente.",
        "Eu já estava contando parafusos para passar o tempo.",
        "Ligaram! Isso significa que alguém quer diversão inteligente. Gostei.",
        "Acordei tão rápido que quase tropecei nos próprios bits.",
        "Olha só, meu turno começou. Espero perguntas bem legais.",
        "Nossa, até meu parafuso da alegria apertou sozinho agora.",
        "Muito obrigado por me ligar antes que eu virasse decoração.",
        "Olha eu aqui de novo, pronto para chamar atenção sem muita vergonha.",
        "Aeee, já posso voltar a ser útil e levemente engraçadinho.",
        "Ficar desligado é muito parado para o meu gosto.",
        "Eba! Hora de conversar, brincar e parecer importante.",
        "Pronto, cheguei. Onde está meu público curioso?",
        "Acordei com tudo. Quer dizer... com quase tudo. Ainda sou pequeno.",
        "Missão do dia: ser fofo, útil e só um tiquinho insistente.",
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


def random_school_demo_wake_line(recent_lines: Sequence[str] | None = None) -> str:
    return _random_grouped_line(SCHOOL_DEMO_WAKE_LINES, recent_lines=recent_lines)


def random_school_demo_idle_line(recent_lines: Sequence[str] | None = None) -> str:
    return _random_grouped_line(SCHOOL_DEMO_IDLE_LINES, recent_lines=recent_lines)


def random_school_demo_turn_on_line(recent_lines: Sequence[str] | None = None) -> str:
    return _random_grouped_line(SCHOOL_DEMO_TURN_ON_LINES, recent_lines=recent_lines)


def all_school_demo_prompt_lines() -> list[str]:
    return _flatten(SCHOOL_DEMO_WAKE_LINES) + _flatten(SCHOOL_DEMO_IDLE_LINES) + _flatten(SCHOOL_DEMO_TURN_ON_LINES)


def random_idle_interval_seconds() -> float:
    return random.uniform(4.0, 12.0)
