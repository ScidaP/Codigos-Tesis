# ======= 1. CPU - Una sola fila por corrida =======
archivo="$1/cpu.csv"
RUN_ID=$2

# Crear encabezado solo si no existe
if [ ! -f "$archivo" ]; then
  echo "run;cycles;instructions;cache-references;cache-misses" > "$archivo"
fi

# Ejecutar perf y capturar métricas
read -r cycles instructions cache_ref cache_miss <<< $(perf stat -e cycles,instructions,cache-references,cache-misses -a sleep 5 2>&1 \
  | grep -E 'cycles|instructions|cache' \
  | awk '{gsub(/\./, "", $1); print $1}' | tr '\n' ' ')

# Agregar la fila con RUN_ID y métricas
echo "$RUN_ID;$cycles;$instructions;$cache_ref;$cache_miss" >> "$archivo"
