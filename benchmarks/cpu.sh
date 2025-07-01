#!/bin/bash

# ========== PARÁMETROS ==========
output_dir="$1"
RUN_ID="$2"
archivo="$output_dir/cpu.csv"

# ========== ENCABEZADO ==========
if [ ! -f "$archivo" ]; then
  echo "run;cycles;instructions;cache-references;cache-misses;r_avg;in_avg;cs_avg;us_avg;sy_avg;id_avg;st_avg;usr_core_avg;idle_core_avg;load1;load5;load15;r_avg_processes;running_avg" > "$archivo"
fi

# ========== PERF STATS ==========
read -r cycles instructions cache_ref cache_miss <<< $(perf stat -e cycles,instructions,cache-references,cache-misses -a sleep 5 2>&1 \
  | grep -E 'cycles|instructions|cache' \
  | awk '{gsub(/\./, "", $1); print $1}' | tr '\n' ' ')

# ========== VMSTAT ==========
vmstat_output=$(vmstat 1 5 | tail -n +3)

read -r r_avg in_avg cs_avg us_avg sy_avg id_avg st_avg <<< $(echo "$vmstat_output" | awk '{
  r_sum += $1; in_sum += $11; cs_sum += $12;
  us_sum += $13; sy_sum += $14; id_sum += $15; st_sum += $17;
}
END {
  count = NR;
  printf "%.2f %.2f %.2f %.2f %.2f %.2f %.2f", r_sum/count, in_sum/count, cs_sum/count, us_sum/count, sy_sum/count, id_sum/count, st_sum/count;
}' | tr ',' '.')

# ========== MPSTAT ==========
mpstat_output=$(mpstat -P ALL 1 5 | grep -E '^[0-9]+' | grep -v 'CPU')

total_cores=0
total_usr=0
total_idle=0

while read -r line; do
  usr=$(echo "$line" | awk '{print $(NF-6)}' | sed 's/,/./' | sed 's/[^0-9.]//g')
  idle=$(echo "$line" | awk '{print $(NF)}'     | sed 's/,/./' | sed 's/[^0-9.]//g')


  if [[ -n "$usr" && -n "$idle" ]]; then
    total_cores=$((total_cores + 1))
    total_usr=$(echo "$total_usr + $usr" | bc)
    total_idle=$(echo "$total_idle + $idle" | bc)
  fi
done <<< "$mpstat_output"

if [ "$total_cores" -gt 0 ]; then
  usr_avg=$(echo "scale=2; $total_usr / $total_cores" | bc)
  idle_avg=$(echo "scale=2; $total_idle / $total_cores" | bc)
else
  usr_avg=0.0
  idle_avg=0.0
fi

# ========== LOAD AVERAGE ==========
read load1 load5 load15 <<< $(uptime | awk -F'load average: ' '{print $2}' | tr ',' '.' | awk '{print $1, $2, $3}' | sed 's/\([0-9]\)\.\([[:space:]]\|$\)/\1\2/g')
# ========== PROCESOS RUNNING ==========
running_total=0
samples=5

for i in $(seq 1 $samples); do
  running_now=$(ps -eo stat | grep -c '^R')
  running_total=$((running_total + running_now))
  sleep 1
done

running_avg=$(echo "scale=2; $running_total / $samples" | bc)

# ========== GUARDAR EN CSV ==========
echo "$RUN_ID;$cycles;$instructions;$cache_ref;$cache_miss;$r_avg;$in_avg;$cs_avg;$us_avg;$sy_avg;$id_avg;$st_avg;$usr_avg;$idle_avg;$load1;$load5;$load15;$r_avg;$running_avg" >> "$archivo"