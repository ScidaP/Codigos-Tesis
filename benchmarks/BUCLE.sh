#!/bin/bash

# Carpeta de resultados por parámetro o por defecto
CARPETA_RESULTADOS="${1:-resultados_csv}"
CANTIDAD_ITERACIONES=$2

echo "====================================="
echo "🔁 Iniciando $2 corridas de benchmarks"
echo "📂 Carpeta de salida: $CARPETA_RESULTADOS"
echo "====================================="
echo ""

for i in $(seq 1 $2); do
    echo "🚀 Iniciando RUN $i..."
    ./CORRER_TODO.sh "$CARPETA_RESULTADOS" "$i"
    echo "✅ RUN $i completado."
    echo "-------------------------------------"
    sleep 1  # Espera opcional de 1 segundos entre corridas
done

echo ""
echo "🎉 Finalizadas las $2 corridas de benchmark"
echo "📄 Resultados disponibles en: $CARPETA_RESULTADOS"
