#!/bin/bash
# medir_recursos.sh

mkdir -p resultados

echo "Medición de CPU..."
perf stat -e cycles,instructions,cache-references,cache-misses -a sleep 5 &> resultados/cpu.txt

echo "Medición de Memoria..."

vmstat 1 5 > resultados/memoria_vmstat.txt
lat_mem_rd 128M 512 > resultados/memoria_latencia.txt 2>&1
stream > resultados/memoria_throughput.txt 2>&1

echo "Medición de Almacenamiento (fio)..."
fio --name=test-readwrite --rw=randrw --bs=4k --size=100M --numjobs=1 --runtime=10 --group_reporting > resultados/almacenamiento_fio.txt

echo "Medición de Red..."
iperf3 -c 192.168.100.15 -t 10 > resultados/red_iperf.txt 2>&1
mtr -r -c 10 8.8.8.8 > resultados/red_mtr.txt

echo "Mediciones completas. Los resultados están en la carpeta 'resultados/'."
