# KidRobo — passo a passo para baixar, instalar e validar no Raspberry Pi

## Objetivo
Este guia foi escrito para permitir uma instalação reprodutível do KidRobo a partir do GitHub em uma Raspberry Pi, com foco em deixar o sistema pronto para testes e demo.

## 1. Pré-requisitos
Você vai precisar de:
- Raspberry Pi 4 com Raspberry Pi OS
- internet ativa
- caixa de som já funcionando no sistema
- microfone USB conectado
- acesso ao GitHub do repositório `Vieirapa/KidRobo`
- chave SSH configurada na Raspberry para clonar o repositório privado

## 2. Validar acesso básico à Raspberry
No seu computador, conecte via SSH:

```bash
ssh <usuario>@<ip-da-raspberry>
```

Depois confirme o sistema:

```bash
uname -a
python3 --version
git --version
```

## 3. Validar acesso ao GitHub
Ainda na Raspberry:

```bash
ssh -T git@github.com
```

Resultado esperado:
- o GitHub reconhece seu usuário e não pede senha interativa do git clone

## 4. Clonar o projeto

```bash
cd ~
git clone git@github.com:Vieirapa/KidRobo.git
cd KidRobo
```

## 5. Dar permissão aos scripts

```bash
chmod +x scripts/*.sh
```

## 6. Executar a instalação automática

```bash
./scripts/install_kidrobo_rpi.sh git@github.com:Vieirapa/KidRobo.git
```

## 7. O que o instalador faz
O script deve:
- instalar dependências de sistema
- criar ambiente virtual Python
- instalar dependências Python
- instalar `feh` e `fbi`
- instalar ou validar o Ollama
- baixar o modelo `qwen2.5:0.5b`
- deixar os scripts auxiliares executáveis

## 8. Ativar o ambiente manualmente (se precisar)

```bash
source ~/.venv/bin/activate
```

Se o repositório foi instalado em `~/KidRobo`, use:

```bash
source ~/KidRobo/.venv/bin/activate
```

## 9. Rodar diagnóstico do ambiente

```bash
cd ~/KidRobo
./scripts/diagnose_kidrobo.sh
```

Verifique especialmente:
- Python e venv OK
- STT carregando
- TTS disponível
- Ollama acessível
- modelo correto presente
- áudio detectado

## 10. Testar áudio

```bash
cd ~/KidRobo
./scripts/test_audio.sh
```

Objetivo do teste:
- confirmar captura do microfone
- confirmar geração do arquivo WAV
- confirmar transcrição básica

## 11. Rodar o KidRobo manualmente

### Modo CLI padrão
```bash
cd ~/KidRobo
./scripts/run_kidrobo.sh
```

### Modo demo
```bash
cd ~/KidRobo
./scripts/run_kidrobo.sh --mode demo
```

### Modo school-demo (quando disponível)
```bash
cd ~/KidRobo
./scripts/run_kidrobo.sh --mode school-demo
```

## 12. Validar display / faces
Se estiver usando a tela:
- coloque assets em `assets/faces/<estado>/`
- prefira resolução 800x480
- teste se `feh` ou `fbi` conseguem mostrar imagens fullscreen

Validação manual sugerida:

```bash
feh -F ~/KidRobo/assets/faces/standby/<arquivo>.png
```

ou

```bash
sudo fbi -T 1 -d /dev/fb0 --noverbose -a ~/KidRobo/assets/faces/standby/<arquivo>.png
```

## 13. Instalar como serviço systemd

```bash
cd ~/KidRobo
./scripts/install_systemd_service.sh
```

Depois:

```bash
systemctl --user daemon-reload
systemctl --user start kidrobo.service
systemctl --user status kidrobo.service
journalctl --user -u kidrobo.service -f
```

## 14. Checklist de bom funcionamento
Considere a plataforma pronta quando estes itens estiverem verdadeiros:

- [ ] Raspberry acessa o GitHub e atualiza o repo
- [ ] ambiente virtual criado
- [ ] `pip install -r software/requirements.txt` sem erro
- [ ] `ollama list` mostra `qwen2.5:0.5b`
- [ ] `diagnose_kidrobo.sh` sem falhas críticas
- [ ] `test_audio.sh` grava e transcreve algo inteligível
- [ ] `run_kidrobo.sh` inicia sem crash
- [ ] TTS fala pelo speaker correto
- [ ] display mostra a face correta
- [ ] serviço systemd sobe com sucesso

## 15. Atualizar o projeto no Raspberry depois
Quando quiser atualizar o código:

```bash
cd ~/KidRobo
git pull --ff-only
source .venv/bin/activate
pip install -r software/requirements.txt
```

Se houver mudanças em serviço/systemd:

```bash
systemctl --user daemon-reload
systemctl --user restart kidrobo.service
```

## 16. Problemas mais prováveis
### GitHub não clona
- revisar chave SSH
- rodar `ssh -T git@github.com`

### Ollama não responde
- checar serviço
- rodar `ollama list`
- testar `curl http://localhost:11434/api/tags`

### Microfone não capta
- revisar dispositivo padrão
- testar com `arecord -l`
- revisar ganho e sample rate

### KidRobo fala, mas não ouve direito
- reduzir volume do speaker
- afastar fisicamente speaker do microfone
- calibrar thresholds e cooldown

## 17. Recomendação operacional para demo
Para a apresentação na escola, a recomendação é:
- usar modo de demo escolar
- testar tudo no local antes do evento
- levar teclado/SSH como contingência
- preparar um roteiro curto de perguntas seguras
