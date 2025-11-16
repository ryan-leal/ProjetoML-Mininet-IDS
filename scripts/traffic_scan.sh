#!/bin/bash
# Scan Nmap focado em TCP (pra bater com o nosso extrator de TCP)

TARGET="10.0.0.1"

PORT_SETS=(
  "1-512"
  "1-1024"
  "1-2048"
  "20-80"
  "80,443,8080,8443"
  "1000-2000"
)

# Só modos TCP:
SCAN_TYPES=(
  "-sS"   # SYN scan (clássico, stealth)
  "-sT"   # TCP connect()
)

TIMINGS=("T2" "T3" "T4" "T5")

SCANS=4   # pode aumentar se quiser mais dados

echo "[INFO] Iniciando $SCANS scans TCP com variabilidade..."

for i in $(seq 1 "$SCANS"); do
  PORTS=${PORT_SETS[$RANDOM % ${#PORT_SETS[@]}]}
  SCAN=${SCAN_TYPES[$RANDOM % ${#SCAN_TYPES[@]}]}
  TIME=${TIMINGS[$RANDOM % ${#TIMINGS[@]}]}

  echo ""
  echo "=== SCAN $i ==="
  echo "[*] Método: $SCAN"
  echo "[*] Portas: $PORTS"
  echo "[*] Timing: $TIME"
  echo "================"

  # -Pn pra não perder tempo com ping ICMP
  nmap $SCAN -Pn -$TIME -p "$PORTS" "$TARGET"
done
