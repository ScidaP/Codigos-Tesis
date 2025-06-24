#!/bin/bash

# ======= 1. CPU - Una sola fila por corrida con vmstat =======
archivo="$1/cpu.csv"
RUN_ID=$2

# Crear encabezado si no existe
if [ ! -f "$archivo" ]; then
  echo "run;cycles;instructions;cache-references;cache-misses;r_avg;in_avg;cs_avg;us_avg;sy_avg;id_avg;st_avg" > "$archivo"
fi

# Ejecutar perf y capturar métricas
read -r cycles instructions cache_ref cache_miss <<< $(perf stat -e cycles,instructions,cache-references,cache-misses -a sleep 5 2>&1 \
  | grep -E 'cycles|instructions|cache' \
  | awk '{gsub(/\./, "", $1); print $1}' | tr '\n' ' ')

# Ejecutar vmstat 1 segundo durante 5 muestras y extraer solo las columnas CPU que necesitamos
vmstat_output=$(vmstat 1 5 | tail -n +3)

read -r r_avg in_avg cs_avg us_avg sy_avg id_avg st_avg <<< $(echo "$vmstat_output" | awk '{
  r_sum += $1; in_sum += $11; cs_sum += $12;
  us_sum += $13; sy_sum += $14; id_sum += $15; st_sum += $17;
}
END {
  count = NR;
  printf "%.2f %.2f %.2f %.2f %.2f %.2f %.2f", r_sum/count, in_sum/count, cs_sum/count, us_sum/count, sy_sum/count, id_sum/count, st_sum/count;
}')

# Escribir al archivo CSV
echo "$RUN_ID;$cycles;$instructions;$cache_ref;$cache_miss;$r_avg;$in_avg;$cs_avg;$us_avg;$sy_avg;$id_avg;$st_avg" >> "$archivo"
