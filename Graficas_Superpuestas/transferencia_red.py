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

# Solo graficar transfer_MB
metrica = "transfer_MB"
label_metrica = "Transferencia"

plt.figure(figsize=(12, 7))

for carpeta in carpetas:
    base_path = os.path.join(resultados_path, carpeta)
    promedios = []

    for u in usuarios:
        path_csv = os.path.join(base_path, f"{u}-Usuarios", "Datos_CSV", "red.csv")
        if not os.path.exists(path_csv):
            print(f"⚠️ Archivo no encontrado: {path_csv}")
            promedios.append(None)
            continue

        df = pd.read_csv(path_csv, delimiter=';')
        df.replace(',', '.', regex=True, inplace=True)

        if metrica in df.columns:
            try:
                df[metrica] = df[metrica].astype(float)
                promedios.append(df[metrica].mean())
            except Exception as e:
                print(f"❌ Error en '{metrica}' de {u} usuarios: {e}")
                promedios.append(None)
        else:
            print(f"❌ Columna '{metrica}' no encontrada en archivo {u} usuarios")
            promedios.append(None)

    # ─── Graficar cada carpeta ──────────────────────────────
    plt.plot(usuarios, promedios, marker='o', linestyle='-', label=carpeta)

# Configuración general de la gráfica
plt.title("Comparación de Transferencia de datos según cantidad de usuarios")
plt.xlabel("Cantidad de usuarios")
plt.ylabel("Transferencia (MB)")
plt.xticks(usuarios)  # mostrar 100, 200, ... 1000
plt.grid(True)
plt.legend(title="Carpeta de resultados", fontsize=8)
plt.tight_layout()

# Guardar en archivo
carpeta_graficas = os.path.join(root_dir, 'Resultados', plataforma, 'Graficas_Superpuestas')
os.makedirs(carpeta_graficas, exist_ok=True)
plt.savefig(os.path.join(carpeta_graficas, "Comparacion_Transferencia_Red.png"))

