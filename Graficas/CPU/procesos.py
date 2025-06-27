import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Lista de usuarios
usuarios = [15, 20, 40, 60, 100, 200, 500, 1000, 2000]
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../', 'Resultados')

# Métricas con sus etiquetas descriptivas
metricas = {
    'r_avg': 'Procesos en cola',
    'in_avg': 'Interrupciones por segundo',
    'cs_avg': 'Cambios de contexto por segundo'
}
promedios = {m: [] for m in metricas}

# Leer CSV y calcular promedios
for u in usuarios:
    path_csv = os.path.join(base_path, f"{u}-Usuarios", "Datos_CSV", "cpu.csv")
    if not os.path.exists(path_csv):
        print(f"⚠️ Archivo no encontrado: {path_csv}")
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

for m, label in metricas.items():
    plt.plot(x, promedios[m], marker='o', label=label)

plt.title("Métricas de tiempo promedio del CPU según cantidad de usuarios")
plt.xlabel("Cantidad de Usuarios Simultáneos")
plt.ylabel("Valor Promedio")
plt.xticks(x, usuarios, rotation=45)

# Eje Y con formato limpio
ax = plt.gca()
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}'))

plt.grid(True)
plt.legend()
plt.tight_layout()
#plt.savefig("grafico_tiempos_promedio_cpu.png")
plt.show()
