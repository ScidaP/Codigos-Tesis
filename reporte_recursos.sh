#!/bin/bash

# Carpeta de resultados: primer parámetro o 'resultados' por defecto
CARPETA="${1:-resultados}"

echo "========== REPORTE DE MEDICIONES =========="
echo ""

echo "Mostrando resultados en la carpeta: $CARPETA"
echo ""

echo "--------------------------------------"
echo "CPU"
echo "--------------------------------------"
echo ""

grep -E 'cycles|instructions|cache' "$CARPETA/cpu.txt" | sed 's/^/  /'
echo ""

echo "--------------------------------------"
echo "Memoria"
echo "--------------------------------------"
echo ""

echo " *** Estadísticas del sistema *** "
echo ""
head -n 10 "$CARPETA/memoria_vmstat.txt" | sed 's/^/  /'
echo ""
echo " *** Latencia *** "
echo ""
cat "$CARPETA/memoria_latencia.txt" | sed 's/^/  /'
echo " *** Throughput *** "
echo ""
awk '/General statistics/ {found=1} found' "$CARPETA/memoria_throughput.txt" | sed 's/^/  /'
echo ""

echo "--------------------------------------"
echo "Almacenamiento"
echo "--------------------------------------"
echo ""
grep -E 'read:|write:|iops=|lat' "$CARPETA/almacenamiento_fio.txt" | sed 's/^/  /'
echo ""

echo "--------------------------------------"
echo "Red"
echo "--------------------------------------"
echo ""

echo " *** Ancho de banda *** "
echo ""
grep -E 'receiver|sender' "$CARPETA/red_iperf.txt" | sed 's/^/  /'
echo ""
echo " *** Latencia *** "
echo ""
cat "$CARPETA/red_mtr.txt" | sed 's/^/  /'
echo ""
echo " *** PPS (Packets Per Second) *** "
echo ""
cat "$CARPETA/red_pps_bmon.txt" | sed 's/^/  /'
