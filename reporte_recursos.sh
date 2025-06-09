#!/bin/bash

echo "========== REPORTE DE MEDICIONES =========="
echo ""

echo "--------------------------------------"
echo "CPU"
echo "--------------------------------------"
echo ""

grep -E 'cycles|instructions|cache' resultados/cpu.txt | sed 's/^/  /'
echo ""

echo "--------------------------------------"
echo "Memoria"
echo "--------------------------------------"
echo ""

echo " *** Estadísticas del sistema *** "
echo ""
head -n 10 resultados/memoria_vmstat.txt | sed 's/^/  /'
echo ""
echo " *** Latencia *** "
echo ""
cat resultados/memoria_latencia.txt | sed 's/^/  /'
echo " *** Throughput *** "
echo ""
awk '/General statistics/ {found=1} found' resultados/memoria_throughput.txt | sed 's/^/  /'
echo ""

echo "--------------------------------------"
echo "Almacenamiento"
echo "--------------------------------------"
echo ""
grep -E 'read:|write:|iops=|lat' resultados/almacenamiento_fio.txt | sed 's/^/  /'
echo ""

echo "--------------------------------------"
echo "Red"
echo "--------------------------------------"
echo ""

echo " *** Ancho de banda *** "
echo ""
grep -E 'receiver|sender' resultados/red_iperf.txt | sed 's/^/  /'
echo ""
echo " *** Latencia *** "
echo ""
cat resultados/red_mtr.txt | sed 's/^/  /'
echo ""
echo " *** PPS (Packets Per Second) *** "
echo ""
cat resultados/red_pps_bmon.txt | sed 's/^/  /'