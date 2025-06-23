#!/bin/bash

archivo="$1/red_pps_bmon.csv"
RUN_ID=$2

if [ ! -f "$archivo" ]; then
  echo "run;interfaz;rx_pps;tx_pps" > "$archivo"
fi

echo "Medición de PPS con bmon..."

# Obtener interfaz predeterminada
interfaz=$(ip -o -4 route show to default | awk '{print $5}')
echo "Interfaz detectada: $interfaz"

# Ejecutar bmon y capturar salida
output=$(timeout 5 bmon -o ascii -p "$interfaz" 2>&1)

# Buscar las líneas que contengan la interfaz y valores PPS
# Ejemplo de línea: "Rx packets:  12345 B"
# Aquí se asume que la salida ASCII muestra PPS de forma que hay que adaptar el parsing

# Como bmon varía, una opción es buscar solo números en líneas relacionadas a la interfaz
# Suponiendo que el output tiene líneas con “Rx PPS:” y “Tx PPS:”
# Si no, probar con regex para extraer números.

rx_pps=$(echo "$output" | grep -i "rx" | grep -oE '[0-9]+' | head -1)
tx_pps=$(echo "$output" | grep -i "tx" | grep -oE '[0-9]+' | head -1)

# Si no se encontró nada, poner 0
rx_pps=${rx_pps:-0}
tx_pps=${tx_pps:-0}

echo "$RUN_ID;$interfaz;$rx_pps;$tx_pps" >> "$archivo"
