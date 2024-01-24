# Ejercicio 3 - GitLab Pipeline
Un pipeline en GitLab es un conjunto automatizado de procesos que se ejecutan en respuesta a cambios en el código fuente de un proyecto. Está definido en un archivo llamado .gitlab-ci.yml y consta de trabajos (jobs) que realizan tareas específicas, como construir, probar y desplegar una aplicación. Estos trabajos se organizan en etapas (stages) y se ejecutan en un entorno controlado por instancias llamadas runners. Los pipelines se activan mediante eventos como la creación de ramas, la apertura de solicitudes de fusión o la programación de ejecuciones periódicas. La configuración del pipeline y sus trabajos se define en el archivo YAML, permitiendo una automatización flexible y escalable del desarrollo, integración continua y despliegue continuo.
## Configuración inicial
Se especifica la imagen de Docker que se utilizará para poder ejecutar el pipeline.
```yaml
image: python:3.9 
```

## Definición de Stages
En esta sección se especificarán las estapas del pipeline, cada una agrupa un conjunto de tareas.
```yaml
stages:
  - prepare
  - execute
#  - publish
  - create
  - insert
  - documentation
```

## Preparación
Se clonará el repositorio de GitLab, para poder realizarlo debemos crear un token "$tokenGITLAB" para poder darle los privilegios y así poder realizar las operaciones.
```yaml
prepare:
  stage: prepare
  script:
    - git clone https://oauth2:$tokenGITLAB@gitlab.com/vs9820852/vsGitLab.git 
```

## Ejecucuión archivo Python
Se deberá instalar las dependencias para poder ejecutar el programa "grafica" la cual convierte y genera los datos a un grafico denominado "grafico.png", este archivo se conservará para etapas posteriores del pipeline en la sección de "artifacts".
```yaml
execute:
  stage: execute
  script:
    - pip install pandas matplotlib
    - python grafica.py 
  artifacts:
    paths:
      - grafico.png
```

## Creación README
Se concatenará el contenido de "documentacion.txt" con el archivo "README2" y como en el apartado anterior se conservará los archivos README2 y grafico.png para etapas posteriores del pipeline en la sección de "artifacts".
```yaml
createReadme:
  stage: create
  script:
    - cat documentacion.txt >> README2.md
  artifacts:
    paths:
      - README2.md
      - grafico.png
```

## Insercción de la imagen
Se insertará la imagen png en el archivo "README2" y como en el apartado anterior se conservará los archivos README2 y grafico.png para etapas posteriores del pipeline en la sección de "artifacts".
```yaml
insertImage:
  stage: insert
  script:
    - echo '![My Image](./grafico.png)' >> README2.md
  artifacts:
    paths:
      - README2.md
      - grafico.png
```

## Crear Documentación
Esta etapa de documentación instala Pandoc, lo utiliza para convertir el contenido de "README2" a un archivo de documentación HTML, y conserva tanto el HTML generado como los archivos originales como artefactos para su almacenamiento.
```yaml
documentation:
  stage: documentation
  script:
    - apt-get update 
    - apt-get install -y pandoc
    - pip install pandoc
    - pandoc README2.md -o documentation.html
  artifacts:
    paths:
      - documentation.html
      - README2.md
      - grafico.png
```

## Despliegue en GitHub Pages
Este script es parte de un flujo de despliegue que parece actualizar un repositorio de GitHub con los archivos grafico.png y documentation.html desde un entorno de CI/CD en GitLab. El uso del token de GitHub (${GITHUB_TOKEN}) es clave para la autenticación en GitHub durante la operación de push. Además, la sección comentada al final (only: - main) indica que el despliegue solo se ejecutará cuando haya cambios en la rama main
```yaml
deploy:
  stage: deploy
  script:
    - apt-get update -qy
    - git config --global user.email "falilealp@gmail.com"
    - git config --global user.name "falilp"
    - git clone https://falilp:${GITHUB_TOKEN}@github.com/falilp/falilp.github.io.git
    - cd falilp.github.io
    - cp ../grafico.png ./grafico.png
    - cp ../documentation.html ./index.html
    - git add --all
    - git commit -m "Deploy GitLab"
    - git push -u origin main
#  only:
#    - main
```

## Pipeline 
```yaml
image: python:3.9  # Utiliza la imagen de Python 3.9

stages:
  - prepare
  - execute
#  - publish
  - create
  - insert
  - documentation
  - deploy

prepare:
  stage: prepare
  script:
    - git clone https://oauth2:$tokenGITLAB@gitlab.com/vs9820852/vsGitLab.git  # Clona el repositorio

execute:
  stage: execute
  script:
    - pip install pandas matplotlib
    - python grafica.py  # Ejecuta el script de transformación de datos
  artifacts:
    paths:
      - grafico.png

#publish:
#  stage: publish
#  script:
#    - ls
#    - >
#      curl -v -X POST -H "Authorization: Bearer $FIGSHARE_API_TOKEN" \
#      -F "files[]=grafico.png" \
#      https://api.figshare.com/v2/account/articles
#    - pip install requests
#    - python figshare.py

createReadme:
  stage: create
  script:
    - cat documentacion.txt >> README2.md
  artifacts:
    paths:
      - README2.md
      - grafico.png

insertImage:
  stage: insert
  script:
    - echo '![My Image](./grafico.png)' >> README2.md
  artifacts:
    paths:
      - README2.md
      - grafico.png

documentation:
  stage: documentation
  script:
    - apt-get update 
    - apt-get install -y pandoc
    - pip install pandoc
    - pandoc README2.md -o documentation.html
  artifacts:
    paths:
      - documentation.html
      - README2.md
      - grafico.png

deploy:
  stage: deploy
  script:
    - apt-get update -qy
    - git config --global user.email "falilealp@gmail.com"
    - git config --global user.name "falilp"
    - git clone https://falilp:${GITHUB_TOKEN}@github.com/falilp/falilp.github.io.git
    - cd falilp.github.io
    - cp ../grafico.png ./grafico.png
    - cp ../documentation.html ./index.html
    - git add --all
    - git commit -m "Deploy GitLab"
    - git push -u origin main
#  only:
#    - main
```
## Autores
-Rafael Leal Pardo
-Manuel Coca Alba

## Archvios
https://falilp.github.io/
[Pipeline Ejercicio1](../Ejercicio1/azure-pipelines.yml)
[Documento Pipeline Ejercicio1](../Ejercicio1/Documento.md)
[Pipeline Ejercicio2](../Ejercicio2/azure-pipelines.yml)
[Documento Pipeline Ejercicio2](../Ejercicio2/Documento.md)
[Pipeline Ejercicio3](../Ejercicio3/gitlab-ci.yml)
[grafica.py](../Ejercicio3/grafica.py)