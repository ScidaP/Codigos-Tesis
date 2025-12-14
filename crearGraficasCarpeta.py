import os
import sys
import subprocess

# Primer parámetro: carpeta de datos dentro de Resultados/Proxmox/
carpeta_datos = sys.argv[1]
# Segundo parámetro: nombre de la carpeta donde se guardan las gráficas en Resultados/Proxmox/
carpeta_graficas = sys.argv[2]

def ejecutar_scripts_en_carpeta(base_path):
    # Lista las subcarpetas dentro de base_path
    subcarpetas = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    
    for subcarpeta in subcarpetas:
        ruta_subcarpeta = os.path.join(base_path, subcarpeta)
        print(f"\nEjecutando scripts en la carpeta: {ruta_subcarpeta}")
        
        # Lista todos los archivos .py en la subcarpeta
        archivos_py = [f for f in os.listdir(ruta_subcarpeta) if f.endswith('.py')]
        
        for archivo in archivos_py:
            ruta_script = os.path.join(ruta_subcarpeta, archivo)
            print(f"Ejecutando {ruta_script} ...")
            # Ejecuta el script con python pasando ambos parámetros
            resultado = subprocess.run(['python', ruta_script, carpeta_datos, carpeta_graficas], capture_output=True, text=True)
            
            if resultado.returncode == 0:
                print(f"Ejecutado correctamente: {archivo}")
            else:
                print(f"Error al ejecutar {archivo}:")
                print(resultado.stderr)

if __name__ == "__main__":
    carpeta_scripts = "Graficas"
    ejecutar_scripts_en_carpeta(carpeta_scripts)

