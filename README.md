# Archivos usados para el desarrollo de mi tesis de Licenciatura #

### En este repositorio guardaré todos los códigos que voy a usar para el desarrollo de mi tesis de Licenciatura en Informática.

La tesis trata sobre montar una aplicación web en distintos servidores físicos y virtualizados, para así simular tráfico y recolectar datos acerca de la perfomance del servidor utilizado.

Finalmente, se reune toda la información para concluir acerca de la mejor opción para montar un servidor. 

### Notas archivos

1. **pruebaEstres.py**
  - Este código se ejecuta en una computadora cliente. Aquí aprovecho la herramienta `Locust`, la cual me permite simular tráfico en mi aplicación. Puedo ajustar la cantidad de usuarios, los endpoints solicitados y la frecuencia de las peticiones a cada uno.
2. **medir_recursos.sh**
  - Este código se ejecuta en el servidor (mediante SSH). Uso herramientas como `perf`, `htop`, `lat_mem_rd`, `stream`, `vmstat`, `fio`, `iperf3`, `mtr` y `bmon`. Todas útiles para monitorear el desempeño del servidor en términos de CPU, memoria, almacenamiento y red bajo una prueba de estrés. El archivo guarda los resultados en archivos de texto en la carpeta `resultados/`.
3. **reporte_recursos.sh**
  - Este código se ejecuta en el servidor (mediante SSH). Lee los archivos de texto guardados en `resultados/` y los imprime por pantalla de manera ordenada, para una mejor visualización.

## Motivación

La virtualización de servidores es una tecnología clave en la administración de infraestructuras informáticas modernas, permitiendo una mejor utilización de los recursos físicos y facilitando la escalabilidad de los servicios. Sin embargo, su implementación introduce una capa de abstracción que puede afectar el rendimiento de las aplicaciones y sistemas alojados. A pesar de los avances en optimización, aún persisten interrogantes sobre el impacto real de la virtualización en diferentes escenarios de uso y sobre la efectividad de las estrategias para mitigar posibles degradaciones en el desempeño.

La presente tesis tiene como objetivo evaluar el impacto de la virtualización en el rendimiento de servidores, comparando distintos hipervisores y estrategias de optimización. Se utilizará una aplicación web para las pruebas de rendimiento, y se analizarán métricas clave como el uso de CPU, memoria, rendimiento de disco y latencia de red en entornos virtualizados, con el fin de identificar diferencias significativas entre soluciones de virtualización y estrategias de optimización aplicadas.

El estudio proporcionará información valiosa para administradores de sistemas, desarrolladores y responsables de infraestructura tecnológica, ayudándolos a tomar decisiones fundamentadas sobre qué tecnologías y configuraciones emplear en función de los requerimientos específicos de sus entornos de trabajo. Además, contribuirá a las Ciencias de la Computación al generar datos empíricos sobre el impacto de la virtualización en el rendimiento y al proponer mejores prácticas para maximizar la eficiencia en entornos virtualizados.
