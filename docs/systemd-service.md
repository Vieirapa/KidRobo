# Serviço systemd do KidRobo

## Objetivo
Executar o KidRobo automaticamente na Raspberry Pi para a demo escolar.

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
- o serviço atual espera 1 segundo após o boot antes de iniciar
- antes de subir o app, ele aplica `Mic 12%` e `Auto Gain Control off`
- o `ExecStart` usa `run_kidrobo.sh --mode school-demo-fluid --no-display`
- isso é focado na apresentação escolar e em subir direto sem depender de teclado
