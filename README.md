# Archivos usados para el desarrollo de mi tesis de Licenciatura #

### En este repositorio guardaré todos los códigos que voy a usar para el desarrollo de mi tesis de Licenciatura en Informática.

La tesis trata sobre montar una aplicación web en distintos servidores físicos y virtualizados, para así simular tráfico y recolectar datos acerca de la perfomance del servidor utilizado.

Finalmente, se reune toda la información para concluir acerca de la mejor opción para montar un servidor. 

### Aclaraciones archivos importantes

## Simulación y recolección de datos

1. **proceso_completo.ps1**
  - Se ejecuta la siguiente secuencia por cada cantidad de usuarios: *I.* Limpiar tabla de pedidos (`borrar.sql`), *II.* Empezar simulación de usuarios (`pruebaEstres.py`), *III.* Recolectar datos sobre el desempeño del servidor (`benchmarks/BUCLE.sh`, se ejecuta en el servidor), *IV.* Copiar esos datos del servidor a mi notebook (comando `scp`), y *V.* Limpiar aquellas conexiones que quedaron abiertas (`cerrar_conexiones.sql`). Este código se encarga de ejecutar dicha secuencia. 
2. **pruebaEstres.py**
  - Este código se ejecuta en una computadora cliente. Aquí aprovecho la herramienta `Locust`, la cual me permite simular tráfico en mi aplicación. Puedo ajustar la cantidad de usuarios, los endpoints solicitados y la frecuencia de las peticiones a cada uno.
3. **cerrar_conexiones.sql, borrar.sql**
  - Consultas SQL que se ejecutan en el código `proceso_completo.ps1`.

## Visualización de datos
1. **crearGraficasSuperpuestas.py** 
  - Recibe un parámetro: {Proxmox|Debian}. Corresponde a la carpeta dentro de `/Resultados`. El archivo crea las gráficas superpuestas usando TODOS los datos recolectados de la carpeta elegida. Por ejemplo, si se lo corre para Debian, usa todos los datos de `/Resultados/Debian/` para crear la gráfica superpuesta, ignorando los archivos que no son de datos (los que empiezan con la palabra "Graficas" del mismo directorio)
2. **crearGraficasTodas**
  - Recibe un parámetro: {Proxmox|Debian}. Misma idea que el archivo anterior. Pero en lugar de crear gráficas superpuestas, crea las gráficas de cada test en particular. Por ejemplo, cuando ejecuta sobre la carpeta `/Resultados/Debian/08-12`, ejecuta todos los scripts de la carpeta `/Graficas/` para ese test en particular.
3. **crearGraficasCarpeta.py**
  - Recibe dos parámetros: El nombre de la carpeta del test, y el nombre de la carpeta donde se guardarán las nuevas gráficas de ese test.

## Motivación

La virtualización de servidores es una tecnología clave en la administración de infraestructuras informáticas modernas, permitiendo una mejor utilización de los recursos físicos y facilitando la escalabilidad de los servicios. Sin embargo, su implementación introduce una capa de abstracción que puede afectar el rendimiento de las aplicaciones y sistemas alojados. A pesar de los avances en optimización, aún persisten interrogantes sobre el impacto real de la virtualización en diferentes escenarios de uso y sobre la efectividad de las estrategias para mitigar posibles degradaciones en el desempeño.

La presente tesis tiene como objetivo evaluar el impacto de la virtualización en el rendimiento de servidores, comparando distintos hipervisores y estrategias de optimización. Se utilizará una aplicación web para las pruebas de rendimiento, y se analizarán métricas clave como el uso de CPU, memoria, rendimiento de disco y latencia de red en entornos virtualizados, con el fin de identificar diferencias significativas entre soluciones de virtualización y estrategias de optimización aplicadas.

El estudio proporcionará información valiosa para administradores de sistemas, desarrolladores y responsables de infraestructura tecnológica, ayudándolos a tomar decisiones fundamentadas sobre qué tecnologías y configuraciones emplear en función de los requerimientos específicos de sus entornos de trabajo. Además, contribuirá a las Ciencias de la Computación al generar datos empíricos sobre el impacto de la virtualización en el rendimiento y al proponer mejores prácticas para maximizar la eficiencia en entornos virtualizados.
