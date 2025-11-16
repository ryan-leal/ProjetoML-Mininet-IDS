#!/bin/bash
# Tráfego HTTP "humano" simplificado, sem python3 nem base64

TARGET="10.0.0.1"
PORT="8080"
BASE_URL="http://$TARGET:$PORT"

REQUESTS=80

PATHS=(
  "/"
  "/index.html"
  "/home"
  "/login"
  "/logout"
  "/products"
  "/products?id=1"
  "/products?id=2"
  "/search?q=test"
  "/search?q=foo"
  "/profile"
)

USER_AGENTS=(
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/125.0"
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
  "Mozilla/5.0 (Linux; Android 13; SM-G990B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"
)

# pausa curta aleatória entre 0.2 e 1.0 segundos
rand_sleep_short() {
  local ms=$((RANDOM % 800 + 200))  # 200–999 ms
  sleep "0.$ms"
}

for i in $(seq 1 "$REQUESTS"); do
  PATH_REQ=${PATHS[$RANDOM % ${#PATHS[@]}]}
  UA=${USER_AGENTS[$RANDOM % ${#USER_AGENTS[@]}]}

  # Só GET por enquanto, pra não depender de payloads aleatórios
  curl -s -A "$UA" "$BASE_URL$PATH_REQ" > /dev/null

  rand_sleep_short

  # De vez em quando dá um “pensar” mais longo na página
  if (( RANDOM % 20 == 0 )); then
    sleep $((RANDOM % 4 + 2))  # 2–5s
  fi
done
