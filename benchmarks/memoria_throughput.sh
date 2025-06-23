#!/bin/bash

archivo="$1/memoria_throughput.csv"
RUN_ID=$2

# Crear archivo con encabezado si no existe
if [ ! -f "$archivo" ]; then
  echo "run;threads;block_size;total_size;operation;total_operations;total_time_s;min_latency_ms;avg_latency_ms;max_latency_ms" > "$archivo"
fi

echo "Ejecutando prueba de Throughput de Memoria con sysbench..."

# Ejecutar sysbench
output=$(sysbench memory --memory-block-size=1M --memory-total-size=128M run 2>&1)

# Extraer información
threads=1
block_size=$(echo "$output" | grep "block size" | awk -F: '{print $2}' | xargs)
total_size=$(echo "$output" | grep "total size" | awk -F: '{print $2}' | xargs)
operation="write"  # Sysbench memory test usa escritura por defecto
total_operations=$(echo "$output" | grep "Total operations:" | awk '{print $3}')
total_time=$(echo "$output" | grep "total time:" | awk '{print $3}' | sed 's/s//')

# Latencias
min_latency=$(echo "$output" | awk '/Latency \(ms\)/{getline; print $2}')
avg_latency=$(echo "$output" | awk '/avg:/{print $2}')
max_latency=$(echo "$output" | awk '/max:/{print $2}')

# Validar que todos existan (si no, poner 0)
min_latency=${min_latency:-0}
avg_latency=${avg_latency:-0}
max_latency=${max_latency:-0}

# Guardar en el archivo
echo "$RUN_ID;$threads;$block_size;$total_size;$operation;$total_operations;$total_time;$min_latency;$avg_latency;$max_latency" >> "$archivo"
