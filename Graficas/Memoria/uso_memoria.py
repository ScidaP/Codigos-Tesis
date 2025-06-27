import os
import pandas as pd
import matplotlib.pyplot as plt

usuarios = [15, 20, 40, 60, 100, 200, 500, 1000, 2000]
base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Resultados')

metricas_memoria = {
    'buff_avg': 'Buffers usados',
    'cache_avg': 'Memoria en caché'
}

promedios = {k: [] for k in metricas_memoria}

for u in usuarios:
    path_csv = os.path.join(base_path, f"{u}-Usuarios", "Datos_CSV", "memoria.csv")
    if not os.path.exists(path_csv):
        print(f"⚠️ Archivo no encontrado: {path_csv}")
        for k in metricas_memoria:
            promedios[k].append(None)
        continue

    df = pd.read_csv(path_csv, delimiter=';')
    df.columns = df.columns.str.strip()
    df.replace(',', '.', regex=True, inplace=True)

    # Solo intentar convertir las columnas necesarias
    for col in metricas_memoria:
        if col in df.columns:
            try:
                df[col] = df[col].astype(float) / 1024
                promedios[col].append(df[col].mean())
            except Exception as e:
                print(f"❌ Error en '{col}' de {u} usuarios: {e}")
                promedios[col].append(None)
        else:
            print(f"❌ Columna '{col}' no encontrada en archivo {u} usuarios")
            promedios[col].append(None)

# ─── Gráfico ───────────────────────────────────────

x = list(range(len(usuarios)))
plt.figure(figsize=(12, 6))

for k, label in metricas_memoria.items():
    plt.plot(x, promedios[k], marker='o', label=label)

plt.title("Uso de Memoria - 20 muestras por cantidad de usuario")
plt.xlabel("Cantidad de Usuarios Simultáneos")
plt.ylabel("Megabytes (MB)")
plt.xticks(x, usuarios)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("Memoria-Uso.png")