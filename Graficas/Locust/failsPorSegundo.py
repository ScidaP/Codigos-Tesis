import csv
import os
import sys
import matplotlib.pyplot as plt

# Rutas base y configuración
nombre_carpeta = sys.argv[1]
usuarios_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
requests_per_second = []

for usuarios in usuarios_list:
    file_path = os.path.join('Resultados/' + nombre_carpeta, f"{usuarios}-Usuarios", "Locust", "data_stats.csv")
    
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                if row.get("Name", "").strip() == "Aggregated":
                    requests = float(row["Failures/s"].replace(",", "."))
                    requests_per_second.append(requests)
                    break
    except FileNotFoundError:
        print(f"Archivo no encontrado: {file_path}")
        requests_per_second.append(0)

# Para espaciado uniforme en X
x_positions = list(range(len(usuarios_list)))

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(x_positions, requests_per_second, marker='o', linestyle='-', color='blue')
plt.title("Promedio de errores por segundo por cantidad de usuarios")
plt.xlabel("Cantidad de usuarios")
plt.ylabel("Errores por segundo")
plt.grid(True)
plt.xticks(x_positions, usuarios_list)  # Muestra los valores reales como etiquetas
plt.tight_layout()

os.makedirs(nombre_carpeta, exist_ok=True) 
plt.savefig(nombre_carpeta + "/failsPorSegundo.png")
