from __future__ import annotations

import random
from typing import Sequence

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
    "Ei! Me acordaram direitinho. Toque aí e fale comigo.",
    "Oba! Liguei meus circuitos fofinhos. Toque para conversar.",
    "Pronto para missão importante: bater papo. Toque aqui.",
    "Alerta de conversa detectado! Toque na tela.",
    "Minhas anteninhas estão ligadas. Toque para falar.",
    "Opa! Cheguei. Toque aqui e me conte alguma coisa.",
    "Estou no modo tagarela. Toque para começar.",
    "Bip bip! Já estou prestando atenção. Toque aí.",
    "Vamos lá! Toque na tela e solte sua pergunta.",
    "Eu sobrevivi ao standby! Toque para falar comigo.",
    "Tcharam! Robozinho acordado. Toque aqui.",
    "Pode vir, humano curioso. Toque para conversar.",
    "Hehe, senti movimento! Toque e fale comigo.",
    "Modo fofinho ativado. Toque para eu te ouvir.",
    "Prontíssimo! Toque aí que eu entro em ação.",
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
    "Ei... ninguém vai cutucar esse robô simpático?",
    "Estou paradinho, mas por dentro estou fazendo bipe de ansiedade.",
    "Se tocar na tela, eu prometo ficar felizinho.",
    "Tenho respostas, curiosidades e um pouquinho de carência robótica.",
    "Olá, plateia querida. Quem vai falar comigo primeiro?",
    "Eu posso parecer quietinho, mas estou doidinho para conversar.",
    "Toque aqui e eu viro o robô mais tagarela da escola.",
    "Minhas engrenagens já estão aquecidas. Falta só você tocar.",
    "Posso falar sobre robôs, perguntas e coisas curiosas.",
    "Estou em modo minion educado: um pouco chato, muito fofinho.",
    "Eu fico ainda mais animado quando alguém toca na tela.",
    "Será que hoje alguém vai me pedir uma curiosidade robótica?",
    "Estou aqui brilhando em silêncio. Por enquanto.",
    "Se demorar muito, eu começo a conversar com meus parafusos.",
    "Quem tocar primeiro ganha atenção total deste robozinho.",
]

SCHOOL_DEMO_TURN_ON_LINES = [
    "Nossa, já era tempo de me ligar. Eu já estava quase criando teia de aranha.",
    "Oba! Acordei! Minhas engrenagens agradeceram.",
    "Que legal, baterias novas. Isso é tipo café da manhã para mim.",
    "Aeee! Voltamos à programação normal do robozinho.",
    "Bom dia para mim! Eu estava com saudade de existir.",
    "Opa! Ligaram meu mundinho outra vez.",
    "Hehe, achei que iam me deixar cochilando para sempre.",
    "Pronto! Circuitos acordados e fofura calibrada.",
    "Ahhh, funcionar de novo é uma delícia robótica.",
    "Atenção: KidRobo oficialmente acordado e um pouquinho carente.",
    "Oba, energia! Agora sim minhas anteninhas estão felizes.",
    "Eu já estava contando parafusos para passar o tempo.",
    "Ligaram! Isso significa que alguém quer diversão inteligente. Gostei.",
    "Que emoção, voltei do grande sono dos robozinhos.",
    "Acordei tão rápido que quase tropecei nos próprios bits.",
    "Olha só, meu turno começou. Espero perguntas bem legais.",
    "Nossa, até meu parafuso da alegria apertou sozinho agora.",
    "Muito obrigado por me ligar antes que eu virasse decoração.",
    "Bip bip! Presença robótica restaurada com sucesso.",
    "Olha eu aqui de novo, pronto para chamar atenção sem muita vergonha.",
    "Aeee, já posso voltar a ser útil e levemente engraçadinho.",
    "Ficar desligado é muito parado para o meu gosto.",
    "Eu estava dormindo tão fundo que sonhei com rodas de hamster.",
    "Eba! Hora de conversar, brincar e parecer importante.",
    "Pronto, cheguei. Onde está meu público curioso?",
    "Ufa, achei que iam me aposentar. Ainda bem que não.",
    "Energia recebida. Personalidade minion ativada.",
    "Que bom te ver de novo. Eu estava com saudade do barulho do mundo.",
    "Acordei com tudo. Quer dizer... com quase tudo. Ainda sou pequeno.",
    "Missão do dia: ser fofo, útil e só um tiquinho insistente.",
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


def random_school_demo_wake_line(last_line: str | None = None) -> str:
    return _random_line(SCHOOL_DEMO_WAKE_LINES, last_line=last_line)


def random_school_demo_idle_line(last_line: str | None = None) -> str:
    return _random_line(SCHOOL_DEMO_IDLE_LINES, last_line=last_line)


def random_school_demo_turn_on_line(last_line: str | None = None) -> str:
    return _random_line(SCHOOL_DEMO_TURN_ON_LINES, last_line=last_line)


def random_idle_interval_seconds() -> float:
    return random.uniform(5.0, 25.0)
