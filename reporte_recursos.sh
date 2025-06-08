#!/bin/bash

echo "========== REPORTE DE MEDICIONES =========="
echo ""

echo "CPU"
grep -E 'cycles|instructions|cache' resultados/cpu.txt | sed 's/^/  /'
echo ""

echo "Memoria"

echo "- Estadísticas del sistema:"
head -n 10 resultados/memoria_vmstat.txt | sed 's/^/  /'
echo "- Latencia:"
grep "avg" resultados/memoria_latencia.txt | sed 's/^/  /'
echo "- Throughput:"
grep -A 3 "Function" resultados/memoria_throughput.txt | sed 's/^/  /'
echo ""

echo "Almacenamiento (IOPS, Latencia)"
grep -E 'read:|write:|iops=|lat' resultados/almacenamiento_fio.txt | sed 's/^/  /'
echo ""

echo "Red"
echo "- Ancho de banda (iperf3):"
grep -E 'receiver|sender' resultados/red_iperf.txt | sed 's/^/  /'
echo "- Latencia (mtr):"
tail -n 10 resultados/red_mtr.txt | sed 's/^/  /'

echo ""
echo "Reporte generado con datos de la carpeta 'resultados/'."
