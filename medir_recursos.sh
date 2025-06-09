#!/bin/bash
# medir_recursos.sh

# Buscar la carpeta resultados1 a resultados5 disponible o rotar
max=5
carpeta_resultados=""
for i in $(seq 1 $max); do
  carpeta="resultados$i"
  if [ ! -d "$carpeta" ]; then
    carpeta_resultados=$carpeta
    break
  fi
done

# Si todas existen, rotar y usar resultados1 (borrando antes)
if [ -z "$carpeta_resultados" ]; then
  carpeta_resultados="resultados1"
  rm -rf "$carpeta_resultados"
fi

mkdir -p "$carpeta_resultados"

echo "Guardando resultados en la carpeta $carpeta_resultados"

echo "Medición de CPU..."
perf stat -e cycles,instructions,cache-references,cache-misses -a sleep 5 &> "$carpeta_resultados/cpu.txt"

echo "Medición de Memoria..."
vmstat 1 5 > "$carpeta_resultados/memoria_vmstat.txt"

echo "Medición de Latencia de Memoria con lmbench..."
/usr/lib/lmbench/bin/x86_64-linux-gnu/lat_mem_rd 128M 16777216 > "$carpeta_resultados/memoria_latencia.txt" 2>&1

echo "Medición de Throughput de Memoria con sysbench..."
sysbench memory --memory-block-size=1M --memory-total-size=128M run > "$carpeta_resultados/memoria_throughput.txt" 2>&1

echo "Medición de Almacenamiento (fio)..."
fio --name=test-readwrite --rw=randrw --bs=4k --size=100M --numjobs=1 --runtime=10 --group_reporting > "$carpeta_resultados/almacenamiento_fio.txt"

echo "Medición de Red..."
iperf3 -c 192.168.100.15 -t 10 > "$carpeta_resultados/red_iperf.txt" 2>&1
mtr -r -c 10 8.8.8.8 > "$carpeta_resultados/red_mtr.txt"

echo "Medición de PPS con bmon..."
timeout 5 bmon -o ascii -p $(ip -o -4 route show to default | awk '{print $5}') > "$carpeta_resultados/red_pps_bmon.txt" 2>&1

echo "Mediciones completas. Los resultados están en la carpeta '$carpeta_resultados'."