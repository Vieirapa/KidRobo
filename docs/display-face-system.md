# Sistema de rosto em tela do KidRobo

## Objetivo
Preparar o KidRobo para usar a tela touch 800x480 da Raspberry Pi como rosto do personagem, exibindo imagens full-screen que mudam conforme o estado emocional/operacional.

## Conceito
Cada estado do KidRobo aponta para um diretório com imagens correspondentes. O sistema escolhe imagens aleatórias desse estado e as exibe em tela cheia.

## Estados previstos
- `standby`
- `happy`
- `talking`
- `angry`
- `afraid`
- `waiting`
- `error`

## Comportamento esperado
### Standby
Exibir aleatoriamente frames do diretório `assets/faces/standby/`.

### Talking
Alternar aleatoriamente frames de `assets/faces/talking/` durante a fala, simulando boca/expressão em movimento.

### Waiting
Usar imagens de `assets/faces/waiting/` enquanto estiver aguardando a próxima interação.

### Angry / Afraid / Error
Permitir estados especiais para emoções e exceções futuras.

## Arquitetura implementada
### Módulos
- `software/app/display/state_catalog.py`
- `software/app/display/face_assets.py`
- `software/app/display/renderer.py`
- `software/app/display/manager.py`

### Responsabilidades
- catálogo de estados visuais
- carregamento dos assets por estado
- seleção aleatória de frames
- renderização full-screen via `fbi` ou `feh`

## Renderização inicial
O sistema está preparado para usar:
- `fbi` em framebuffer (`/dev/fb0`)
- ou `feh` em ambiente gráfico/X11

## Estratégia recomendada na Raspberry Pi
### Fase 1
Usar `feh -F` se estiver rodando desktop/X11.

### Fase 2
Se o projeto virar appliance dedicado, testar `fbi` diretamente no framebuffer para fullscreen limpo e boot mais controlado.

## Próxima evolução sugerida
- cache das listas de imagens por estado
- prevenção de repetição imediata do mesmo frame
- integração com toque na tela
- transição suave entre estados
- sincronização da troca de imagens com TTS
