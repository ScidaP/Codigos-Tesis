import os
import pandas as pd
import matplotlib.pyplot as plt

# Carpetas a procesar
carpetas = ["08-12", "08-12_2", "08-12_3", 
            "08-16", "08-16_2", "08-16_3", 
            "08-17", "08-17_2", "08-17_3", 
            "08-18", "08-18_2", "08-18_3"]

usuarios = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

plt.figure(figsize=(12, 7))

for carpeta in carpetas:
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../Resultados/', carpeta)

    promedios = {'cycles': [], 'instructions': []}

    for u in usuarios:
        path_csv = os.path.join(base_path, f"{u}-Usuarios", "Datos_CSV", "cpu.csv")
        if not os.path.exists(path_csv):
            print(f"⚠️ Archivo no encontrado: {path_csv}")
            promedios['cycles'].append(None)
            promedios['instructions'].append(None)
            continue

        df = pd.read_csv(path_csv, delimiter=';')
        df.replace(',', '.', regex=True, inplace=True)
        for col in df.columns:
            if col != 'run':
                df[col] = df[col].astype(float)

        for m in promedios.keys():
            promedios[m].append(df[m].mean() if m in df.columns else None)

    # Calcular IPC = instrucciones / ciclos
    ipc = []
    for ins, cyc in zip(promedios['instructions'], promedios['cycles']):
        if cyc and cyc != 0:
            ipc.append(ins / cyc)
        else:
            ipc.append(None)

    # Graficar cada curva de IPC
    plt.plot(usuarios, ipc, marker='o', linestyle='-', label=carpeta)

# Configuración general de la gráfica
plt.title("Comparación de IPC según cantidad de usuarios")
plt.xlabel("Cantidad de usuarios")
plt.ylabel("IPC (Instructions per Cycle)")
plt.grid(True)
plt.xticks(usuarios)  # mostrar 100, 200, ... 1000
plt.legend(title="Carpeta de resultados")
plt.tight_layout()

# Guardar en archivo
os.makedirs("Graficas", exist_ok=True)
plt.savefig("Graficas/Comparacion_IPC.png")
plt.show()
