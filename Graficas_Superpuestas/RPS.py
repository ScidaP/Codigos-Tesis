import csv
import os
import matplotlib.pyplot as plt

# Obtener todas las carpetas en Resultados/Proxmox/ (excluyendo las que empiezan con "Graficas_")
script_dir = os.path.dirname(os.path.abspath(__file__))
# Subir un nivel desde Graficas_Superpuestas/ a la raíz del proyecto
root_dir = os.path.dirname(script_dir)
proxmox_path = os.path.join(root_dir, 'Resultados', 'Proxmox')
todas_las_carpetas = [f for f in os.listdir(proxmox_path) 
                      if os.path.isdir(os.path.join(proxmox_path, f)) 
                      and not f.startswith('Graficas_')]

carpetas = sorted(todas_las_carpetas)  # Ordenar para consistencia

usuarios_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

plt.figure(figsize=(12, 7))

for carpeta in carpetas:
    requests_per_second = []

    for usuarios in usuarios_list:
        file_path = os.path.join(proxmox_path, carpeta, f"{usuarios}-Usuarios", "Locust", "data_stats.csv")
        
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=",")
                for row in reader:
                    if row.get("Name", "").strip() == "Aggregated":
                        requests = float(row["Requests/s"].replace(",", "."))
                        requests_per_second.append(requests)
                        break
        except FileNotFoundError:
            print(f"Archivo no encontrado: {file_path}")
            requests_per_second.append(0)

    # Graficar cada curva con etiqueta de la carpeta
    plt.plot(usuarios_list, requests_per_second, marker='o', linestyle='-', label=carpeta)

# Configuración general de la gráfica
plt.title("Comparación de Requests/s según cantidad de usuarios")
plt.xlabel("Cantidad de usuarios")
plt.ylabel("Requests por segundo")
plt.grid(True)
plt.xticks(usuarios_list)  # fuerza a mostrar 100, 200, ... 1000
plt.legend(title="Carpeta de resultados")
plt.tight_layout()

# Guardar en un archivo de salida
carpeta_graficas = os.path.join(root_dir, 'Resultados', 'Proxmox', 'Graficas_Superpuestas')
os.makedirs(carpeta_graficas, exist_ok=True)
plt.savefig(os.path.join(carpeta_graficas, "Comparacion_RPS.png"))

