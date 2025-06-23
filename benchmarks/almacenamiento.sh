#!/bin/bash

archivo="$1/almacenamiento.csv"
RUN_ID=$2

if [ ! -f "$archivo" ]; then
  echo "run;read_iops;write_iops" > "$archivo"
fi

output=$(fio --name=test-readwrite --rw=randrw --bs=4k --size=100M --numjobs=1 --runtime=10 --group_reporting 2>&1)

# Extraer IOPS de lectura y escritura
read_iops=$(echo "$output" | grep -i "read: IOPS=" | head -1 | sed -E 's/.*IOPS=([0-9.]+).*/\1/')
write_iops=$(echo "$output" | grep -i "write: IOPS=" | head -1 | sed -E 's/.*IOPS=([0-9.]+).*/\1/')

# Validar o poner 0 si no se encontró
read_iops=${read_iops:-0}
write_iops=${write_iops:-0}

echo "$RUN_ID;$read_iops;$write_iops" >> "$archivo"
