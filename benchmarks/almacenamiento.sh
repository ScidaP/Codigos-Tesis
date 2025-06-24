#!/bin/bash

# Activar formato numérico con punto decimal
export LC_NUMERIC=C

archivo="$1/almacenamiento.csv"
RUN_ID=$2

# Crear encabezado si no existe
if [ ! -f "$archivo" ]; then
  echo "run;read_iops;write_iops;read_bw_MBps;write_bw_MBps;read_lat_avg_ms;write_lat_avg_ms" > "$archivo"
fi

# Ejecutar fio
output=$(fio --name=test-readwrite --rw=randrw --bs=4k --size=100M --numjobs=1 --runtime=10 --group_reporting)

# === IOPS ===
read_iops=$(echo "$output" | grep -E "^ *read:" | grep -oP 'IOPS=\K[0-9.]+')
write_iops=$(echo "$output" | grep -E "^ *write:" | grep -oP 'IOPS=\K[0-9.]+')

# === BW ===
read_bw=$(echo "$output" | grep -E "^ *read:" | grep -oP 'BW=\K[0-9.]+[KMG]?i?B/s')
write_bw=$(echo "$output" | grep -E "^ *write:" | grep -oP 'BW=\K[0-9.]+[KMG]?i?B/s')

convert_bw_to_MBps() {
  local bw=$1
  if [[ "$bw" =~ ([0-9.]+)([KMG])i?B/s ]]; then
    num=${BASH_REMATCH[1]}
    unit=${BASH_REMATCH[2]}
    case "$unit" in
      K) echo "$(awk "BEGIN {print $num / 1024}")" ;;
      M) echo "$num" ;;
      G) echo "$(awk "BEGIN {print $num * 1024}")" ;;
    esac
  else
    echo "0"
  fi
}

read_bw_MBps=$(convert_bw_to_MBps "$read_bw")
write_bw_MBps=$(convert_bw_to_MBps "$write_bw")

# === Latencias ===
read_lat_us=$(echo "$output" | grep -A2 "read:" | grep "clat (usec)" | grep -oP 'avg=\K[0-9.]+')
write_lat_ns=$(echo "$output" | grep -A2 "write:" | grep "clat (nsec)" | grep -oP 'avg=\K[0-9.]+')

read_lat_avg_ms=$(awk "BEGIN {print $read_lat_us / 1000}")
write_lat_avg_ms=$(awk "BEGIN {print $write_lat_ns / 1000000}")

# Reemplazo de coma decimal por punto (por si acaso)
read_lat_avg_ms=${read_lat_avg_ms/,/.}
write_lat_avg_ms=${write_lat_avg_ms/,/.}
read_bw_MBps=${read_bw_MBps/,/.}
write_bw_MBps=${write_bw_MBps/,/.}

# Valores por defecto si están vacíos
read_iops=${read_iops:-0}
write_iops=${write_iops:-0}
read_bw_MBps=${read_bw_MBps:-0}
write_bw_MBps=${write_bw_MBps:-0}
read_lat_avg_ms=${read_lat_avg_ms:-0}
write_lat_avg_ms=${write_lat_avg_ms:-0}

# Guardar en CSV
echo "$RUN_ID;$read_iops;$write_iops;$read_bw_MBps;$write_bw_MBps;$read_lat_avg_ms;$write_lat_avg_ms" >> "$archivo"
