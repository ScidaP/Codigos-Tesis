import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

usuarios = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
nombre_carpeta = sys.argv[1]
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../Resultados/', nombre_carpeta)
metricas = {
    'read_iops': 'Lecturas por segundo (IOPS)',
    'write_iops': 'Escrituras por segundo (IOPS)'
}
promedios = {m: [] for m in metricas}

# Leer y calcular promedios
for u in usuarios:
    path_csv = os.path.join(base_path, f"{u}-Usuarios", "Datos_CSV", "almacenamiento.csv")
    if not os.path.exists(path_csv):
        print(f"⚠️ Archivo no encontrado: {path_csv}")
        for m in promedios:
            promedios[m].append(None)
        continue

    df = pd.read_csv(path_csv, delimiter=';')
    df.replace(',', '.', regex=True, inplace=True)
    try:
        for col in df.columns:
            if col != 'run':
                df[col] = df[col].astype(float)
        for m in metricas:
            if m in df.columns:
                promedios[m].append(df[m].mean())
            else:
                print(f"❌ Columna faltante: {m} en {path_csv}")
                promedios[m].append(None)
    except Exception as e:
        print(f"❌ Error procesando {path_csv}: {e}")
        for m in promedios:
            promedios[m].append(None)

# ─── GRAFICAR ─────────────────────────────────────────────────────

x = list(range(len(usuarios)))
plt.figure(figsize=(14, 6))

for m, label in metricas.items():
    y = promedios[m]
    plt.plot(x, y, marker='o', label=label)

    # Mostrar valor numérico junto al punto
    for i, val in enumerate(y):
        if val is not None:
            plt.annotate(f'{val:.0f}', (x[i], val), textcoords="offset points", xytext=(10, 10), ha='center', fontsize=9)

plt.title("Operaciones de I/O por segundo (IOPS) - 20 muestras por cantidad de usuario")
plt.xlabel("Cantidad de Usuarios Simultáneos")
plt.ylabel("IOPS promedio")
plt.xticks(x, usuarios, rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

os.makedirs(nombre_carpeta, exist_ok=True) 
plt.savefig(nombre_carpeta + "/Almacenamiento-IOPS.png")