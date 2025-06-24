#!/bin/bash

archivo="$1/red.csv"
RUN_ID=$2

# Crear CSV con encabezado si no existe
if [ ! -f "$archivo" ]; then
  echo "run;transfer_MB;bandwidth_Mbps;hops;avg_loss_pct;avg_latency_ms;avg_best_ms;avg_worst_ms;avg_stdev_ms;interfaz;rx_pps;tx_pps" > "$archivo"
fi

# --- IPERF3 ---
output_iperf=$(iperf3 -c 192.168.100.39 -t 10 2>&1)

linea_iperf=$(echo "$output_iperf" | grep -E "sender" | grep -Eo "[0-9.]+ [MG]Bytes +[0-9.]+ [MG]bits/sec")

transfer=$(echo "$linea_iperf" | awk '{print $1}')
transfer_unit=$(echo "$linea_iperf" | awk '{print $2}')
bandwidth=$(echo "$linea_iperf" | awk '{print $3}')
bandwidth_unit=$(echo "$linea_iperf" | awk '{print $4}')

if [[ "$transfer_unit" == "GBytes" ]]; then
  transfer_MB=$(echo "$transfer * 1024" | bc)
elif [[ "$transfer_unit" == "MBytes" ]]; then
  transfer_MB=$transfer
else
  transfer_MB=0
fi

if [[ "$bandwidth_unit" == "Gbits/sec" ]]; then
  bandwidth_Mbps=$(echo "$bandwidth * 1000" | bc)
elif [[ "$bandwidth_unit" == "Mbits/sec" ]]; then
  bandwidth_Mbps=$bandwidth
else
  bandwidth_Mbps=0
fi

# --- MTR ---
output_mtr=$(mtr -r -c 10 8.8.8.8 2>&1)

hops_lines=$(echo "$output_mtr" | grep -E "^[[:space:]]*[0-9]+\.\|--")

hops_count=$(echo "$hops_lines" | wc -l)

read avg_loss avg_avg avg_best avg_wrst avg_stdev <<< $(echo "$hops_lines" | awk '
{
  gsub(",", ".", $3); gsub(",", ".", $5); gsub(",", ".", $6); gsub(",", ".", $7); gsub(",", ".", $8);
  sum_loss+=$3; sum_avg+=$5; sum_best+=$6; sum_wrst+=$7; sum_stdev+=$8
}
END {
  if (NR > 0)
    printf "%.2f %.2f %.2f %.2f %.2f\n", sum_loss/NR, sum_avg/NR, sum_best/NR, sum_wrst/NR, sum_stdev/NR;
  else
    print "0 0 0 0 0"
}')

# --- BMON ---

interfaz=$(ip -o -4 route show to default | awk '{print $5}')

rx1=$(cat /sys/class/net/$interfaz/statistics/rx_packets)
tx1=$(cat /sys/class/net/$interfaz/statistics/tx_packets)

sleep 1

rx2=$(cat /sys/class/net/$interfaz/statistics/rx_packets)
tx2=$(cat /sys/class/net/$interfaz/statistics/tx_packets)

rx_pps=$((rx2 - rx1))
tx_pps=$((tx2 - tx1))

# --- Guardar todo en el CSV ---

echo "$RUN_ID;$transfer_MB;$bandwidth_Mbps;$hops_count;$avg_loss;$avg_avg;$avg_best;$avg_wrst;$avg_stdev;$interfaz;$rx_pps;$tx_pps" >> "$archivo"
