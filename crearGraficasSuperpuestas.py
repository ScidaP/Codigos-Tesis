import os
import sys
import subprocess

# Parámetro: "Debian" o "Proxmox"
if len(sys.argv) < 2:
    print("Uso: python crearGraficasSuperpuestas.py <Debian|Proxmox>")
    sys.exit(1)

plataforma = sys.argv[1]

if plataforma not in ["Debian", "Proxmox"]:
    print(f"Error: La plataforma debe ser 'Debian' o 'Proxmox'. Se recibió: {plataforma}")
    sys.exit(1)

# Obtener la ruta del script actual y construir la ruta a Graficas_Superpuestas
script_dir = os.path.dirname(os.path.abspath(__file__))
carpeta_scripts = os.path.join(script_dir, 'Graficas_Superpuestas')

# Verificar que la carpeta existe
if not os.path.exists(carpeta_scripts):
    print(f"Error: No se encontró la carpeta {carpeta_scripts}")
    sys.exit(1)

# Lista todos los archivos .py en Graficas_Superpuestas
archivos_py = [f for f in os.listdir(carpeta_scripts) 
               if f.endswith('.py') and os.path.isfile(os.path.join(carpeta_scripts, f))]

if not archivos_py:
    print(f"No se encontraron scripts .py en {carpeta_scripts}")
    sys.exit(0)

archivos_py = sorted(archivos_py)  # Ordenar para consistencia

print(f"Se encontraron {len(archivos_py)} scripts para ejecutar en {carpeta_scripts}")
print(f"Scripts: {', '.join(archivos_py)}\n")
print(f"Plataforma: {plataforma}\n")

# Ejecutar cada script pasándole el parámetro de plataforma
for archivo in archivos_py:
    ruta_script = os.path.join(carpeta_scripts, archivo)
    print(f"\n{'='*60}")
    print(f"Ejecutando: {archivo}")
    print(f"{'='*60}")
    
    # Ejecutar el script con python pasando el parámetro de plataforma
    resultado = subprocess.run(['python', ruta_script, plataforma], capture_output=True, text=True)
    
    if resultado.returncode == 0:
        print(f"✓ Ejecutado correctamente: {archivo}")
        if resultado.stdout:
            print(resultado.stdout)
    else:
        print(f"✗ Error al ejecutar {archivo}:")
        if resultado.stderr:
            print(resultado.stderr)
        if resultado.stdout:
            print(resultado.stdout)

print(f"\n{'='*60}")
print("Proceso completado")
print(f"{'='*60}")

