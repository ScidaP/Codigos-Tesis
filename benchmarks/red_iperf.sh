#!/bin/bash

archivo="$1/red_iperf.csv"
RUN_ID=$2

if [ ! -f "$archivo" ]; then
  echo "run,transfer_MB,bandwidth_Mbps" > "$archivo"
fi

output=$(iperf3 -c 192.168.100.15 -t 10 2>&1)

# Extraer línea que contiene el resumen con "sec" y "Bytes"
linea=$(echo "$output" | grep -E "sec.*Bytes.*bits/sec" | tail -n 1)

# Extraer transferencia y ancho de banda
transfer=$(echo "$linea" | awk '{print $(NF-5), $(NF-4)}')  # ej: "1.10 GBytes"
bandwidth=$(echo "$linea" | awk '{print $(NF-3), $(NF-2)}') # ej: "941 Mbits/sec"

# Convertir transferencia a MB
value=$(echo "$transfer" | awk '{print $1}')
unit=$(echo "$transfer" | awk '{print $2}')

if [[ "$unit" == "GBytes" ]]; then
  transfer_MB=$(echo "$value * 1024" | bc)
elif [[ "$unit" == "MBytes" ]]; then
  transfer_MB=$value
else
  transfer_MB=0
fi

# Convertir bandwidth a Mbps
bw_value=$(echo "$bandwidth" | awk '{print $1}')
bw_unit=$(echo "$bandwidth" | awk '{print $2}')

if [[ "$bw_unit" == "Gbits/sec" ]]; then
  bandwidth_Mbps=$(echo "$bw_value * 1000" | bc)
elif [[ "$bw_unit" == "Mbits/sec" ]]; then
  bandwidth_Mbps=$bw_value
else
  bandwidth_Mbps=0
fi

# Guardar resultado
echo "$RUN_ID,$transfer_MB,$bandwidth_Mbps" >> "$archivo"
