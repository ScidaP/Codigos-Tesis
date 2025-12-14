import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Parámetro: "Debian" o "Proxmox"
plataforma = sys.argv[1] if len(sys.argv) > 1 else "Proxmox"

# Obtener todas las carpetas en Resultados/{plataforma}/ (excluyendo las que empiezan con "Graficas_")
script_dir = os.path.dirname(os.path.abspath(__file__))
# Subir un nivel desde Graficas_Superpuestas/ a la raíz del proyecto
root_dir = os.path.dirname(script_dir)
resultados_path = os.path.join(root_dir, 'Resultados', plataforma)
todas_las_carpetas = [f for f in os.listdir(resultados_path) 
                      if os.path.isdir(os.path.join(resultados_path, f)) 
                      and not f.startswith('Graficas_')]

carpetas = sorted(todas_las_carpetas)  # Ordenar para consistencia

usuarios = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

plt.figure(figsize=(12, 7))

for carpeta in carpetas:
    base_path = os.path.join(resultados_path, carpeta)

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
carpeta_graficas = os.path.join(root_dir, 'Resultados', plataforma, 'Graficas_Superpuestas')
os.makedirs(carpeta_graficas, exist_ok=True)
plt.savefig(os.path.join(carpeta_graficas, "Comparacion_IPC.png"))
