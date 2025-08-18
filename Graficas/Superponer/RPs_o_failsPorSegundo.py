import csv
import os
import matplotlib.pyplot as plt

## CAMBIAR LINEA 28 EN CASO DE NECESITAR RPS

# Carpetas a procesar
carpetas = ["08-12", "08-12_2", "08-12_3", 
            "08-16", "08-16_2", "08-16_3", 
            "08-17", "08-17_2", "08-17_3", 
            "08-18", "08-18_2", "08-18_3"]

usuarios_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

plt.figure(figsize=(12, 7))

for carpeta in carpetas:
    requests_per_second = []

    for usuarios in usuarios_list:
        file_path = os.path.join("Resultados", carpeta, f"{usuarios}-Usuarios", "Locust", "data_stats.csv")
        
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

    # Graficar cada curva con etiqueta de la carpeta
    plt.plot(usuarios_list, requests_per_second, marker='o', linestyle='-', label=carpeta)

# Configuración general de la gráfica
plt.title("Comparación de Errores/s según cantidad de usuarios")
plt.xlabel("Cantidad de usuarios")
plt.ylabel("Errores por segundo")
plt.grid(True)
plt.xticks(usuarios_list)  # <<--- fuerza a mostrar 100, 200, ... 1000
plt.legend(title="Carpeta de resultados")
plt.tight_layout()

# Guardar en un archivo de salida
os.makedirs("Graficas", exist_ok=True)
plt.savefig("Graficas/Comparacion_RPS.png")
plt.show()