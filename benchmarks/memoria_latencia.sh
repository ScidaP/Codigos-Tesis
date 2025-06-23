#!/bin/bash

archivo="$1/memoria_latencia.csv"
RUN_ID=$2

if [ ! -f "$archivo" ]; then
  echo "run;latencia_ns_promedio" > "$archivo"
fi

# Ejecutar lat_mem_rd y capturar salida (con debug para revisar)
output=$(/usr/lib/lmbench/bin/x86_64-linux-gnu/lat_mem_rd 128M 16777216 2>&1)

echo "=== Salida lat_mem_rd ==="
echo "$output"
echo "========================"

# Extraer la latencia promedio de las líneas que siguen a "stride"
lat_promedio=$(echo "$output" | awk '
  /stride/ {getline; sum+=$1; count++}
  END {
    if (count>0)
      print sum/count
    else
      print 0
  }
')

echo "$RUN_ID;$lat_promedio" >> "$archivo"
