# KidRobo — checklist pré-demo

Use esta lista antes de apresentar o KidRobo na escola.

## 1. Energia e boot
- [ ] Raspberry Pi liga normalmente
- [ ] fonte está estável
- [ ] tela inicia corretamente
- [ ] sistema sobe sem travar

## 2. Áudio
- [ ] microfone USB reconhecido
- [ ] caixa de som/bluetooth conectada
- [ ] volume do speaker adequado
- [ ] `Auto Gain Control` do microfone USB está desligado
- [ ] ganho manual do microfone USB está em **25%** (ajuste empírico atual mais promissor)
- [ ] microfone capta voz infantil a curta distância
- [ ] transcrição continua inteligível com esse ajuste no ambiente real
- [ ] KidRobo não está se ouvindo excessivamente

## 3. Software
- [ ] repositório atualizado com `git pull --ff-only`
- [ ] ambiente virtual ok
- [ ] `diagnose_kidrobo.sh` sem falhas críticas
- [ ] `test_audio.sh` funcionando
- [ ] Ollama respondendo
- [ ] modelo `qwen2.5:0.5b` disponível

## 4. Face / display
- [ ] assets presentes nas pastas de estados
- [ ] a face de standby aparece na tela
- [ ] estado de speaking muda visualmente
- [ ] estado de waiting fica perceptível

## 5. Demo escolar
- [ ] `school-demo mode` inicia sem crash
- [ ] push-to-talk simulado funciona
- [ ] o robô responde em frases curtas
- [ ] perguntas infantis comuns caem em resposta local
- [ ] fallback continua educado quando não entende

## 6. Perguntas de palco recomendadas
- [ ] qual é seu nome?
- [ ] quem fez você?
- [ ] você é de verdade?
- [ ] você é meu amigo?
- [ ] você gosta de dinossauros?
- [ ] você sabe contar?
- [ ] você conhece a Maria Antonia?

## 7. Plano B
- [ ] teclado acessível
- [ ] SSH acessível
- [ ] script de execução conhecido
- [ ] operador sabe reiniciar o app rapidamente
