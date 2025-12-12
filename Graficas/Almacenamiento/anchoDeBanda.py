import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

usuarios = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
carpeta_datos = sys.argv[1]  # Carpeta de datos dentro de Resultados/Proxmox/
carpeta_graficas_nombre = sys.argv[2]  # Nombre de carpeta para guardar gráficas en Resultados/Proxmox/
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../Resultados/Proxmox/', carpeta_datos)
metricas = {
    'read_bw_MBps': 'Lectura (MB/s)',
    'write_bw_MBps': 'Escritura (MB/s)'
}
promedios = {m: [] for m in metricas}

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
    plt.plot(x, promedios[m], marker='s', label=label)

plt.title("Ancho de banda de lectura/escritura - 10 muestras por cantidad de usuario")
plt.xlabel("Cantidad de Usuarios Simultáneos")
plt.ylabel("MB/s promedio")
plt.xticks(x, usuarios, rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

# Crear carpeta para guardar
carpeta_graficas = os.path.join('Resultados', 'Proxmox', carpeta_graficas_nombre)
os.makedirs(carpeta_graficas, exist_ok=True) 
plt.savefig(os.path.join(carpeta_graficas, "Almacenamiento-AnchoBanda.png"))
