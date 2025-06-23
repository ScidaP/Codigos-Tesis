#!/bin/bash

archivo="$1/memoria_vmstat.csv"
RUN_ID=$2

# Encabezado CSV si no existe
if [ ! -f "$archivo" ]; then
  echo "run;r_avg;b_avg;swpd_avg;free_avg;buff_avg;cache_avg;si_avg;so_avg;bi_avg;bo_avg;in_avg;cs_avg;us_avg;sy_avg;id_avg;wa_avg;st_avg" > "$archivo"
fi

# Ejecutar vmstat durante 5 segundos (5 muestras)
output=$(vmstat 1 5 | tail -n +3)

# Calcular promedios por columna
promedios=$(echo "$output" | awk '{
  for (i=1; i<=NF; i++) sum[i]+=$i
}
END {
  for (i=1; i<=NF; i++) {
    avg = sum[i]/NR;
    printf "%.2f", avg;
    if (i<NF) printf ";";
  }
}')

# Escribir al CSV
echo "$RUN_ID;$promedios" >> "$archivo"
