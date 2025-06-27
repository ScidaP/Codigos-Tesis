import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

usuarios = [15, 20, 40, 60, 100, 200, 500, 1000, 2000]
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../', 'Resultados')

metricas = ['cycles', 'instructions']
promedios = {m: [] for m in metricas}

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

# ─── Calcular IPC ─────────────────────────────────────────────────────────────

ipc = []
for ins, cyc in zip(promedios['instructions'], promedios['cycles']):
    if cyc and cyc != 0:
        ipc.append(ins / cyc)
    else:
        ipc.append(None)

# ─── GRAFICAR ────────────────────────────────────────────────────────────────

factor = 1e10  # Escala base para cycles/instructions

x = list(range(len(usuarios)))
fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot cycles e instructions (escalados)
for m in metricas:
    valores_escalados = [v / factor for v in promedios[m]]
    ax1.plot(x, valores_escalados, marker='o', label=m)

# Eje Y para IPC
ax2 = ax1.twinx()
ax2.plot(x, ipc, marker='s', linestyle='--', color='red', label='IPC')
ax2.set_ylabel("IPC", color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Formato del eje Y principal
def formato_multiplicador(x, _):
    return f"{x:.2f} × 10¹⁰"

ax1.yaxis.set_major_formatter(ticker.FuncFormatter(formato_multiplicador))
ax1.set_ylabel("Valor Promedio (cycles / instructions)")
ax1.set_xlabel("Cantidad de Usuarios Simultáneos")
ax1.set_xticks(x)
ax1.set_xticklabels(usuarios, rotation=45)
ax1.grid(True)

# Leyendas
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title("Cycles, Instructions e IPC según cantidad de usuarios")
plt.tight_layout()
#plt.savefig("grafico_cycles_instructions_ipc.png")
plt.show()