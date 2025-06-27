import os
import pandas as pd
import matplotlib.pyplot as plt

usuarios = [15, 20, 40, 60, 100, 200, 500, 1000, 2000]
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Resultados')

# Columnas que vamos a graficar
latencias = {
    'min_latency_ms': 'Latencia mínima',
    'avg_latency_ms': 'Latencia promedio',
    'max_latency_ms': 'Latencia máxima'
}
promedios = {k: [] for k in latencias}

for u in usuarios:
    path_csv = os.path.join(base_path, f"{u}-Usuarios", "Datos_CSV", "memoria.csv")
    if not os.path.exists(path_csv):
        print(f"⚠️ No encontrado: {path_csv}")
        for m in promedios:
            promedios[m].append(None)
        continue

    df = pd.read_csv(path_csv, delimiter=';')
    df.replace(',', '.', regex=True, inplace=True)

    for col in latencias:
        try:
            df[col] = df[col].astype(float)
            promedios[col].append(df[col].mean())
        except Exception as e:
            print(f"❌ Error con columna '{col}' en archivo {u} usuarios: {e}")
            promedios[col].append(None)

# ─── Gráfico ─────────────────────────────────────────────────────

x = list(range(len(usuarios)))
plt.figure(figsize=(12, 6))

for k, label in latencias.items():
    y = promedios[k]
    plt.plot(x, y, marker='o', label=label)

plt.title("Latencias de Memoria - 20 muestras por cantidad de usuario. Escritura: bloques de 1024Kib.")
plt.xlabel("Cantidad de Usuarios Simultáneos")
plt.ylabel("Milisegundos")
plt.xticks(x, usuarios)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("Memoria-Latencia.png")