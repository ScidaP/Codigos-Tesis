#!/bin/bash

CARPETA_RESULTADOS="${1:-resultados_csv}"
RUN_ID="${2:-1}"

mkdir -p "$CARPETA_RESULTADOS"

echo "========================"
echo "  INICIANDO MEDICIONES"
echo "  Carpeta: $CARPETA_RESULTADOS"
echo "  RUN_ID: $RUN_ID"
echo "========================"
echo ""

# === CPU ===
echo "➡️  Ejecutando benchmark de CPU..."
./cpu.sh "$CARPETA_RESULTADOS" "$RUN_ID"
echo "✅ CPU completado."
echo ""

# === MEMORIA ===
echo "➡️  Ejecutando benchmarks de MEMORIA..."
./memoria.sh "$CARPETA_RESULTADOS" "$RUN_ID"
echo "✅ Benchmarks de MEMORIA completados."
echo ""

# === ALMACENAMIENTO ===
echo "➡️  Ejecutando benchmark de ALMACENAMIENTO..."
./almacenamiento.sh "$CARPETA_RESULTADOS" "$RUN_ID"
echo "✅ Benchmark de ALMACENAMIENTO completado."
echo ""

# === RED ===
echo "➡️  Ejecutando benchmarks de RED..."
./red.sh "$CARPETA_RESULTADOS" "$RUN_ID"
echo "✅ Benchmarks de RED completados."
echo ""

echo "========================"
echo "✅ TODAS LAS MEDICIONES FINALIZADAS"
echo "  Archivos CSV generados en: $CARPETA_RESULTADOS"
echo "========================"
