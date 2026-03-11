# Assets visuais do KidRobo

Esta pasta guarda os rostos/imagens exibidos na tela do KidRobo.

## Resolução alvo
- **800 x 480** pixels
- preferencialmente PNG
- fundo consistente para evitar cintilação visual

## Estrutura esperada
```text
assets/faces/
├── standby/
├── happy/
├── talking/
├── angry/
├── afraid/
├── waiting/
└── error/
```

## Regras
- cada pasta representa um estado visual
- você pode colocar várias imagens por estado
- o sistema escolherá imagens aleatórias do diretório correspondente
- durante estados animados, como `talking`, o KidRobo alternará imagens do estado para simular movimento facial

## Sugestão de mapeamento inicial
- `standby/` → dormindo / neutro
- `happy/` → ouvindo / ativado / sorrindo
- `talking/` → falando
- `angry/` → bravo
- `afraid/` → medo / assustado
- `waiting/` → aguardando nova mensagem / pensando
- `error/` → erro / confuso

## Convenção sugerida de nomes
```text
frame-01.png
frame-02.png
frame-03.png
```
