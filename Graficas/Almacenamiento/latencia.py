import os
import pandas as pd
import matplotlib.pyplot as plt

# Lista de usuarios evaluados
usuarios = [15, 20, 40, 60, 100, 200, 500, 1000, 2000]
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../', 'Resultados')

# Métricas a graficar
metricas_latencia = {
    'read_lat_avg_ms': 'Latencia promedio de lectura (ms)',
    'write_lat_avg_ms': 'Latencia promedio de escritura (ms)'
}

# Inicializar estructura de promedios
promedios = {m: [] for m in metricas_latencia}

# Leer archivos y calcular promedios
for u in usuarios:
    path_csv = os.path.join(base_path, f"{u}-Usuarios", "Datos_CSV", "almacenamiento.csv")
    if not os.path.exists(path_csv):
        print(f"⚠️ Archivo no encontrado: {path_csv}")
        for m in promedios:
            promedios[m].append(None)
        continue

    df = pd.read_csv(path_csv, delimiter=';')
    df.replace(',', '.', regex=True, inplace=True)
    for col in df.columns:
        if col != 'run':
            df[col] = df[col].astype(float)

    for m in metricas_latencia:
        promedios[m].append(df[m].mean() if m in df.columns else None)

# ─── GRAFICAR LATENCIAS ─────────────────────────────────────────────────────

x = list(range(len(usuarios)))
plt.figure(figsize=(14, 6))

for m, label in metricas_latencia.items():
    plt.plot(x, promedios[m], marker='o', linestyle='-', label=label)

plt.title("Latencias promedio de lectura y escritura")
plt.xlabel("Cantidad de Usuarios Simultáneos")
plt.ylabel("Latencia (ms)")
plt.xticks(x, usuarios, rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
