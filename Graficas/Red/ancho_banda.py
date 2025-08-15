import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

usuarios = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
nombre_carpeta = sys.argv[1]
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../Resultados/', nombre_carpeta)

# Columnas que vamos a graficar
latencias = {
    'transfer_MB': 'Transferencia',
    'bandwidth_Mbps': 'Ancho de banda',
}
promedios = {k: [] for k in latencias}

for u in usuarios:
    path_csv = os.path.join(base_path, f"{u}-Usuarios", "Datos_CSV", "red.csv")
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

plt.title("Datos transferidos en 10 segundos - 20 muestras por cantidad de usuario")
plt.xlabel("Cantidad de Usuarios Simultáneos")
plt.ylabel("Megabytes (MB)")
plt.xticks(x, usuarios)
plt.grid(True)
plt.legend()
plt.tight_layout()

os.makedirs(nombre_carpeta, exist_ok=True) 
plt.savefig(nombre_carpeta + "/Red-AnchoBanda.png")