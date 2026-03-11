# Estratégia de uso do Ollama no KidRobo

## Objetivo
Usar um modelo pequeno via Ollama para dar respostas mais interessantes no MVP, sem perder previsibilidade e sem matar a Raspberry Pi 4 de cansaço.

## Modelo recomendado para começar
### `qwen2.5:0.5b`
Motivos:
- pequeno o suficiente para testes iniciais em Raspberry Pi 4
- mais leve que modelos de 1B+
- tende a ser utilizável com latência mais aceitável
- bom como primeiro experimento para perguntas abertas simples

## Segunda opção
### `llama3.2:1b`
Usar apenas se:
- a Pi 4 tiver RAM suficiente
- a latência estiver aceitável
- o ganho de qualidade compensar o custo

## Estratégia de fallback
1. perguntas muito previsíveis usam respostas locais
2. perguntas abertas usam Ollama
3. se Ollama falhar, KidRobo responde com fallback seguro

## Regras para o Ollama
- respostas curtas
- português do Brasil
- linguagem infantil
- sem conteúdo inadequado
- máximo de 1 a 2 frases no MVP

## Comandos típicos de teste
```bash
ollama pull qwen2.5:0.5b
ollama run qwen2.5:0.5b
```

## Observação importante
Mesmo usando Ollama, o projeto não deve depender exclusivamente de geração livre. O correto para produto embarcado infantil é manter uma camada local de intenções, regras e segurança.
