#!/bin/bash

archivo="$1/memoria.csv"
RUN_ID=$2

# Crear archivo con encabezado si no existe
if [ ! -f "$archivo" ]; then
  echo "run;latencia_ms_promedio;threads;block_size;total_size;total_operations;total_time_s;min_latency_ms;avg_latency_ms;max_latency_ms;swpd_avg;free_avg;buff_avg;cache_avg;si_avg;so_avg;mem_used;mem_free" > "$archivo"
fi

### === 1. lat_mem_rd ===
output_lat=$(/usr/lib/lmbench/bin/x86_64-linux-gnu/lat_mem_rd 128M 16777216 2>&1)
lat_ns_promedio=$(echo "$output_lat" | awk '
  /stride/ {getline; sum+=$1; count++}
  END {
    if (count>0)
      print sum/count
    else
      print 0
  }
')

# Convertir a milisegundos
lat_ms_promedio=$(awk "BEGIN {printf \"%.6f\", $lat_ns_promedio / 1000000}")

### === 2. sysbench ===
output_sysbench=$(sysbench memory --memory-block-size=1M --memory-total-size=128M run 2>&1)

threads=1
block_size=$(echo "$output_sysbench" | grep "block size" | awk -F: '{print $2}' | xargs)
total_size=$(echo "$output_sysbench" | grep "total size" | awk -F: '{print $2}' | xargs)
total_operations=$(echo "$output_sysbench" | grep "Total operations:" | awk '{print $3}')
total_time=$(echo "$output_sysbench" | grep "total time:" | awk '{print $3}' | sed 's/s//')
min_latency=$(echo "$output_sysbench" | awk '/Latency \(ms\)/{getline; print $2}')
avg_latency=$(echo "$output_sysbench" | awk '/avg:/{print $2}')
max_latency=$(echo "$output_sysbench" | awk '/max:/{print $2}')

# Validar campos vacíos
min_latency=${min_latency:-0}
avg_latency=${avg_latency:-0}
max_latency=${max_latency:-0}

### === 3. vmstat ===
output_vmstat=$(vmstat 1 5 | tail -n +3)
read -r swpd free buff cache si so <<< $(echo "$output_vmstat" | awk '{
  swpd+=$3; free+=$4; buff+=$5; cache+=$6; si+=$7; so+=$8
}
END {
  printf "%.0f %.0f %.0f %.0f %.0f %.0f", swpd/NR, free/NR, buff/NR, cache/NR, si/NR, so/NR
}')

### === 3. free ===

read mem_used mem_free <<< $(free -m | awk '/^Mem:/ {print $3, $4}')

### === Guardar todos los datos en una línea ===
echo "$RUN_ID;$lat_ms_promedio;$threads;$block_size;$total_size;$total_operations;$total_time;$min_latency;$avg_latency;$max_latency;$swpd;$free;$buff;$cache;$si;$so;$mem_used;$mem_free" >> "$archivo"