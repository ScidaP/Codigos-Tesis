#!/bin/bash

archivo="$1/red_mtr.csv"
RUN_ID=$2

if [ ! -f "$archivo" ]; then
  echo "run;hops;avg_loss_pct;avg_latency_ms;avg_best_ms;avg_worst_ms;avg_stdev_ms" > "$archivo"
fi

output=$(mtr -r -c 10 8.8.8.8 2>&1)

# Extraer las líneas de los hops (números al inicio de línea, luego IP)
hops_lines=$(echo "$output" | grep -E "^[[:space:]]*[0-9]+\.\|--")

# Calcular cantidad de hops
hops_count=$(echo "$hops_lines" | wc -l)

# Sumar y calcular promedios con awk, cambiando coma decimal por punto si hace falta
read avg_loss avg_avg avg_best avg_wrst avg_stdev <<< $(echo "$hops_lines" | \
awk '{
  gsub(",", ".", $3); gsub(",", ".", $6); gsub(",", ".", $7); gsub(",", ".", $8); gsub(",", ".", $9);
  sum_loss+=$3; sum_avg+=$6; sum_best+=$7; sum_wrst+=$8; sum_stdev+=$9
}
END {
  printf "%.2f %.2f %.2f %.2f %.2f\n", sum_loss/NR, sum_avg/NR, sum_best/NR, sum_wrst/NR, sum_stdev/NR
}')

echo "$RUN_ID;$hops_count;$avg_loss;$avg_avg;$avg_best;$avg_wrst;$avg_stdev" >> "$archivo"
