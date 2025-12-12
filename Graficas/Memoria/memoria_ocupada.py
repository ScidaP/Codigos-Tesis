import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

usuarios = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
carpeta_datos = sys.argv[1]  # Carpeta de datos dentro de Resultados/Proxmox/
carpeta_graficas_nombre = sys.argv[2]  # Nombre de carpeta para guardar gráficas en Resultados/Proxmox/
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../Resultados/Proxmox/', carpeta_datos)

# Columnas que vamos a graficar
latencias = {
    'mem_free': 'Memoria sin asignar',
    'mem_used': 'Memoria en uso'
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

plt.title("Memoria en Uso en MB")
plt.xlabel("Cantidad de Usuarios Simultáneos")
plt.ylabel("MB")
plt.xticks(x, usuarios)
plt.grid(True)
plt.legend()
plt.tight_layout()

carpeta_graficas = os.path.join('Resultados', 'Proxmox', carpeta_graficas_nombre)
os.makedirs(carpeta_graficas, exist_ok=True) 
plt.savefig(os.path.join(carpeta_graficas, "Memoria-Ocupada.png"))