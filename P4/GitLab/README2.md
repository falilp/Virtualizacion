## Imagen: El pipeline utiliza la imagen de Python 3.9. Esto significa que todas las tareas se ejecutan en un entorno que tiene Python 3.9 instalado.
## Stages: Las etapas del pipeline son prepare, execute, create, insert y documentation. Cada etapa representa una fase distinta del proceso de CI/CD.
## Prepare: En esta etapa, el pipeline clona un repositorio de GitLab. El comando git clone se utiliza para copiar el repositorio completo desde GitLab al ambiente de ejecución del pipeline.
## Execute: Durante esta etapa, el pipeline instala dos paquetes de Python: pandas y matplotlib. Luego, ejecuta un script de Python llamado grafica.py. Finalmente, el pipeline lista todos los archivos en el directorio actual con el comando ls. Los artefactos generados por esta etapa, como el archivo grafico.png, se guardan para su uso en etapas posteriores.
## Create: En esta etapa, el pipeline lee el contenido de un archivo llamado documentacion.txt y lo añade al final de un archivo llamado README2.md.
## Insert: Durante esta etapa, el pipeline añade una línea al archivo README2.md que incrusta la imagen grafico.png.
## Documentation: Finalmente, en esta etapa, el pipeline instala la herramienta pandoc y la utiliza para convertir el archivo README2.md en un archivo HTML llamado documentation.html.![My Image](./grafico.png)
