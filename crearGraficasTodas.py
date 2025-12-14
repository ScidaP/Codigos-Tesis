import os
import sys
import subprocess

# Parámetro: "Debian" o "Proxmox"
if len(sys.argv) < 2:
    print("Uso: python crearGraficasTodas.py <Debian|Proxmox>")
    sys.exit(1)

plataforma = sys.argv[1]

if plataforma not in ["Debian", "Proxmox"]:
    print(f"Error: La plataforma debe ser 'Debian' o 'Proxmox'. Se recibió: {plataforma}")
    sys.exit(1)

# Obtener la ruta del script actual y construir la ruta a Resultados
script_dir = os.path.dirname(os.path.abspath(__file__))
resultados_path = os.path.join(script_dir, 'Resultados', plataforma)

# Verificar que la carpeta existe
if not os.path.exists(resultados_path):
    print(f"Error: No se encontró la carpeta {resultados_path}")
    sys.exit(1)

# Obtener todas las carpetas en Resultados/{plataforma}/ (excluyendo las que empiezan con "Graficas")
todas_las_carpetas = [f for f in os.listdir(resultados_path) 
                      if os.path.isdir(os.path.join(resultados_path, f)) 
                      and not f.startswith('Graficas')]

carpetas = sorted(todas_las_carpetas)  # Ordenar para consistencia

if not carpetas:
    print(f"No se encontraron carpetas en {resultados_path} (excluyendo las que empiezan con 'Graficas')")
    sys.exit(0)

print(f"Se encontraron {len(carpetas)} carpetas para procesar en {resultados_path}")
print(f"Carpetas: {', '.join(carpetas)}\n")

# Ejecutar crearGraficasCarpeta.py para cada carpeta
for carpeta in carpetas:
    nombre_carpeta_graficas = f"Graficas_{carpeta}"
    print(f"\n{'='*60}")
    print(f"Procesando carpeta: {carpeta}")
    print(f"Nombre de carpeta de gráficas: {nombre_carpeta_graficas}")
    print(f"{'='*60}")
    
    # Ejecutar crearGraficasCarpeta.py con los parámetros correspondientes
    comando = ['python', 'crearGraficasCarpeta.py', carpeta, nombre_carpeta_graficas]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    if resultado.returncode == 0:
        print(f"✓ Gráficas creadas exitosamente para {carpeta}")
        if resultado.stdout:
            print(resultado.stdout)
    else:
        print(f"✗ Error al crear gráficas para {carpeta}:")
        print(resultado.stderr)
        if resultado.stdout:
            print(resultado.stdout)

print(f"\n{'='*60}")
print("Proceso completado")
print(f"{'='*60}")

