# Serviço systemd do KidRobo

## Objetivo
Executar o KidRobo automaticamente na Raspberry Pi, inicialmente em modo demo contínuo.

## Instalação
```bash
./scripts/install_systemd_service.sh
```

## Comandos úteis
Iniciar:
```bash
systemctl --user start kidrobo.service
```

Parar:
```bash
systemctl --user stop kidrobo.service
```

Status:
```bash
systemctl --user status kidrobo.service
```

Logs:
```bash
journalctl --user -u kidrobo.service -f
```

## Observações
- o serviço atual usa `run_kidrobo.sh --mode demo --loop`
- isso é ideal para validar boot, áudio e estabilidade básica
- depois podemos trocar o `ExecStart` para o modo principal com wake word real
