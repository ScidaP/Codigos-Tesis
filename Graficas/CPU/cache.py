import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Lista de cantidades de usuarios
usuarios = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
carpeta_datos = sys.argv[1]  # Carpeta de datos dentro de Resultados/{plataforma}/
carpeta_graficas_nombre = sys.argv[2]  # Nombre de carpeta para guardar gráficas en Resultados/{plataforma}/
plataforma = sys.argv[3] if len(sys.argv) > 3 else "Proxmox"
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../Resultados', plataforma, carpeta_datos)

metricas = ['cache-references', 'cache-misses']
promedios = {m: [] for m in metricas}

# Leer los archivos CSV y calcular promedios
for u in usuarios:
    path_csv = os.path.join(base_path, f"{u}-Usuarios", "Datos_CSV", "cpu.csv")
    if not os.path.exists(path_csv):
        print(f"Archivo no encontrado: {path_csv}")
        for m in metricas:
            promedios[m].append(None)
        continue

    df = pd.read_csv(path_csv, delimiter=';')
    df.replace(',', '.', regex=True, inplace=True)
    for col in df.columns:
        if col != 'run':
            df[col] = df[col].astype(float)

    for m in metricas:
        promedios[m].append(df[m].mean() if m in df.columns else None)

# ─── GRAFICAR ────────────────────────────────────────────────────────────────

x = list(range(len(usuarios)))
plt.figure(figsize=(14, 6))

for m in metricas:
    plt.plot(x, promedios[m], marker='o', label=m)

plt.title("Cache References y Cache Misses - 10 muestras por cantidad de usuario")
plt.xlabel("Cantidad de Usuarios Simultáneos")
plt.ylabel("Valor Promedio Absoluto")
plt.xticks(x, usuarios, rotation=45)

# Formato con separadores de miles
ax = plt.gca()
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

plt.grid(True)
plt.legend()
plt.tight_layout()

carpeta_graficas = os.path.join('Resultados', plataforma, carpeta_graficas_nombre)
os.makedirs(carpeta_graficas, exist_ok=True) 
plt.savefig(os.path.join(carpeta_graficas, "CPU-cache.png"))
