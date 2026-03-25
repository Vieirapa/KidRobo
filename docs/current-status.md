# Status executivo do KidRobo

> Documento complementar ao `README.md`, focado em leitura rápida para entender o estágio atual do projeto.

## Resumo executivo
O KidRobo já saiu da fase de ideia e hoje existe como um **protótipo funcional de interação por voz em Raspberry Pi**.

A base principal já está montada:
- fluxo de estados do robô
- captura de áudio
- STT local
- TTS local
- respostas locais com fallback via Ollama
- preparação para rosto visual em tela
- scripts de instalação, execução e diagnóstico

O foco agora não é mais “começar”, e sim **lapidar robustez, UX real e comportamento em hardware real**, especialmente no áudio.

---

## 1. FEITO

### Núcleo da aplicação
- aplicação principal em Python estruturada por módulos
- máquina de estados com fluxo principal do robô
- estados principais de interação: standby, listening, thinking, speaking e error
- execução por CLI para facilitar debug e evolução rápida

### Voz e diálogo
- STT local com `faster-whisper`
- TTS local com `espeak-ng`
- resposta híbrida com:
  - intents/respostas locais
  - fallback para Ollama em perguntas abertas
  - fallback local seguro quando o Ollama falha ou demora
- expansão das intents locais para perguntas infantis comuns
- continuidade básica de conversa após cada resposta
- retorno ao standby por comando explícito ou timeout

### Fluxo de uso
- modo padrão com **captura automática por áudio** após wake
- modo texto preservado para debug
- modo legado com prompt manual preservado para troubleshooting
- logs mais claros para acompanhar a rodada de interação
- instrumentação de latência por etapa

### Raspberry Pi / operação
- script de instalação inicial
- script de execução
- script de teste de áudio
- script de diagnóstico do ambiente
- serviço `systemd` inicial para modo demo
- alinhamento do diagnóstico ao modelo `qwen2.5:0.5b`

### Visual / personagem
- estrutura para rosto por estados visuais
- suporte planejado para imagens 800x480 full-screen
- renderização preparada com `feh` e `fbi`
- estados visuais definidos: standby, happy, talking, angry, afraid, waiting, error

### Decisões técnicas já consolidadas
- Raspberry Pi 4 como referência prática inicial
- `qwen2.5:0.5b` como melhor equilíbrio atual para uso contínuo no Raspberry Pi
- priorização de respostas locais antes do LLM
- priorização de componentes open source
- manutenção do terminal como ferramenta de debug, não como UX final

---

## 2. EM TESTE

### Áudio em hardware real
Itens que já têm implementação parcial ou direção definida, mas ainda precisam de validação prática mais forte na Raspberry Pi real:

- ajuste de sensibilidade do microfone USB
- comportamento da captura em ambientes com ruído real
- thresholds de silêncio e fim de fala
- adaptação de sample rate ao hardware suportado
- consistência da transcrição em uso prolongado

### Experiência de conversa
- janela de continuidade da conversa após resposta
- percepção real de latência entre fala e reação do robô
- frequência com que perguntas simples resolvem localmente sem depender de Ollama
- comportamento do fluxo quando a criança fala fora do timing ideal

### Robustez de fallback
- comportamento quando `webrtcvad` não está disponível
- comportamento quando Ollama falha, demora ou fica indisponível
- experiência prática do fallback local em cenários reais

### Sistema visual
- integração do rosto com a execução real do robô
- uso de assets definitivos em tela
- validação de ritmo e troca de frames durante a fala

---

## 3. PENDENTE

### Prioridade alta
- calibrar melhor ruído, ganho e sensibilidade do microfone
- reduzir autocaptura da própria voz do KidRobo
- melhorar o turn-taking para evitar atropelo entre fala da criança e resposta do robô
- validar uso real em sessões curtas de teste de campo

### Prioridade média
- amadurecer a experiência do rosto visual com assets finais
- sincronizar melhor fala e expressão visual
- revisar timeouts curto/longo de conversa contínua
- validar operação prolongada na Raspberry Pi sem degradação

### Prioridade posterior
- wake word real mais robusta
- LEDs e botão físico
- integração opcional com Arduino
- brincadeiras guiadas mais ricas
- evolução da camada visual/animada do personagem

---

## 4. STATUS POR FRENTE

### Aplicação principal
- **Feito:** base funcional, state machine, diálogo híbrido, fallback resiliente
- **Em teste:** latência percebida, comportamento em hardware real
- **Pendente:** refinamento fino de UX e robustez de campo

### Voz
- **Feito:** STT local, TTS local, fluxo automático após wake
- **Em teste:** thresholds, ruído, sample rate, estabilidade prática
- **Pendente:** autocaptura, turn-taking, validação mais forte com uso real

### Visual
- **Feito:** arquitetura do rosto por estados e mecanismo de renderização preparado
- **Em teste:** integração prática com assets e runtime
- **Pendente:** assets finais, sincronização visual mais refinada

### Operação na Raspberry Pi
- **Feito:** instalação, execução, diagnóstico e serviço demo
- **Em teste:** operação real com dispositivos e ambiente final
- **Pendente:** validação de uso contínuo mais robusto

---

## 5. RISCOS E TRADE-OFFS IMPORTANTES

### O que está bom na abordagem atual
- mantém forte aderência a ferramentas open source
- reduz dependência de cloud para o núcleo da experiência
- facilita debug e evolução incremental
- evita colocar todo o comportamento nas costas do LLM

### O que ainda limita a experiência
- áudio real ainda é o principal gargalo
- TTS atual é robusto, mas não é a voz mais natural possível
- wake word ainda não está no estágio final de produto
- experiência infantil real depende de testes práticos, não só do terminal

### Dependências proprietárias
Até aqui, a espinha dorsal do projeto segue majoritariamente open source. Se forem adotados no futuro:
- vozes premium
- STT premium
- serviços cloud
- assets proprietários

isso deve ser documentado claramente com impacto em custo, portabilidade, autonomia e manutenção.

---

## 6. PRÓXIMOS PASSOS RECOMENDADOS

### Passo 1
Estabilizar a captura de áudio na Raspberry Pi real.

### Passo 2
Calibrar ruído, ganho e thresholds para reduzir falhas de escuta.

### Passo 3
Melhorar a transição entre fala do robô e nova escuta, reduzindo autocaptura.

### Passo 4
Validar pequenas sessões reais de uso para observar timing, latência e previsibilidade.

### Passo 5
Evoluir o rosto visual e depois integrar periféricos físicos.

---

## 7. Leitura recomendada
Para detalhes técnicos e históricos, ver também:
- `README.md`
- `docs/implementation-plan.md`
- `docs/architecture.md`
- `docs/display-face-system.md`
- `docs/raspberry-install.md`
