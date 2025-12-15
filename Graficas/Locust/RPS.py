import csv
import os
import sys
import matplotlib.pyplot as plt

# Rutas base y configuración
carpeta_datos = sys.argv[1]  # Carpeta de datos dentro de Resultados/{plataforma}/
carpeta_graficas_nombre = sys.argv[2]  # Nombre de carpeta para guardar gráficas en Resultados/{plataforma}/
plataforma = sys.argv[3] if len(sys.argv) > 3 else "Proxmox"
usuarios_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
requests_per_second = []

for usuarios in usuarios_list:
    total_requests = 0.0
    
    if plataforma == "Proxmox_Triple_Sucursal":
        # Para Triple Sucursal, sumar los valores de las 3 sucursales
        sucursales = ["Sucursal_229", "Sucursal_242", "Sucursal_243"]
        for sucursal in sucursales:
            file_path = os.path.join('Resultados', plataforma, carpeta_datos, f"{usuarios}-Usuarios", "Locust", sucursal, "data_stats.csv")
            try:
                with open(file_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f, delimiter=",")
                    for row in reader:
                        if row.get("Name", "").strip() == "Aggregated":
                            requests = float(row["Requests/s"].replace(",", "."))
                            total_requests += requests
                            break
            except FileNotFoundError:
                print(f"Archivo no encontrado: {file_path}")
    else:
        # Para otras plataformas, usar la estructura original
        file_path = os.path.join('Resultados', plataforma, carpeta_datos, f"{usuarios}-Usuarios", "Locust", "data_stats.csv")
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=",")
                for row in reader:
                    if row.get("Name", "").strip() == "Aggregated":
                        total_requests = float(row["Requests/s"].replace(",", "."))
                        break
        except FileNotFoundError:
            print(f"Archivo no encontrado: {file_path}")
    
    requests_per_second.append(total_requests)

# Para espaciado uniforme en X
x_positions = list(range(len(usuarios_list)))

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(x_positions, requests_per_second, marker='o', linestyle='-', color='blue')
plt.title("Rendimiento de Requests/s según cantidad de usuarios")
plt.xlabel("Cantidad de usuarios")
plt.ylabel("Requests por segundo (Requests/s)")
plt.grid(True)
plt.xticks(x_positions, usuarios_list)  # Muestra los valores reales como etiquetas
plt.tight_layout()

carpeta_graficas = os.path.join('Resultados', plataforma, carpeta_graficas_nombre)
os.makedirs(carpeta_graficas, exist_ok=True) 
plt.savefig(os.path.join(carpeta_graficas, "RPS.png"))
