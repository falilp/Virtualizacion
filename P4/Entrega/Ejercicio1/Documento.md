# Ejercicio 1 - Azure Pipeline Kubernetes
En Azure, un "pipeline" se refiere a Azure Pipelines, un servicio que automatiza la integración continua y entrega continua (CI/CD). Un pipeline en Azure Pipelines está definido por un archivo YAML o configurado visualmente, y consiste en trabajos y pasos que realizan tareas como compilación, prueba y despliegue. Los agentes ejecutan estos trabajos, y los pipelines pueden desencadenarse por eventos como cambios de código. Azure Pipelines proporciona flexibilidad para gestionar entornos y es esencial para automatizar el desarrollo, pruebas y despliegue de aplicaciones en Azure y otras plataformas.
## Preparación
Para poder realizar el pipeline debemos obtener primero nuestro repositorio en Azure para poder crear en los archivos necesarios de configuración además del pipeline, es necesario configurar SonarQube para que funcione con nuestro repositorio, para ello necesitaremos crear un servicio y crear una máquina virtual en Azure para luego realizar la instalación de SonarQube y su posterior configuración.

Debemos obtener el "cliProjectKey" y "cliProjectName" que debemos de crear con la ayuda de SonarQube para poder ejecutar el mismo en nuestro pipeline.

Para poder realizar la gestión de los paquetes para Kubernetes debemos instalar "Helm" y la herramienta de línea de comandos para interactuar con los clústeres de Kubernetes, "Kubectl". 

Los archivos de configuración necesarios serán los mismos que utilizamos en la práctica de Kubernetes: "kindConfig.yaml", "drupalConfig.yaml" y "mysqlConfig.yaml". Estos archivos deben de estar en nuestro repositorio para poder realizar el pipeline con éxito.

Debemos configurar servicios para poder realizar las conexiones con SonarQube y con el registro de contenedor para poder crear y acceder a los recursos.

## Sección Trigger
La sección "Trigger" determina cuando debe ser ejecutado el pipeline, en nuestro caso será cuando existan cambios como commits, pull request, etc. Cuando se realicen los cambios en la rama "main" de nuestro repositorio.
```yaml
trigger:
- main
```

## Sección Pool

En esta sección especificamos al pool, la imagen que utilizara nuestra máquina virtual para poder ejecutar los "jobs" de nuestro pipeline.
```yaml
pool:
  vmImage: ubuntu-latest
``` 

## Preparar SonarQube
Debemos especificar  el modelo de escáner como en nuestro pipeline 'CLI' ademas de incluir "cliProjectKey" (Llave del proyecto), "cliProjectName" (Nombre del proyecto) y "cliSources" (Ubicación fuente).
```yaml 
- task: SonarQubePrepare@5
  inputs:
    SonarQube: 'SonarK'
    scannerMode: 'CLI'
    configMode: 'manual'
    cliProjectKey: 'vsAzure_vsAzure_AYyld2zCyILi-MNuEvd5'
    cliProjectName: 'vsAzure'
    cliSources: '.'
  displayName: 'Preparando Sonar'
```

## Instalar Helm, Kubectl y desplegar Kubernetes
Se instalarán "Helm" que es un gestor de paquetes para Kubernetes y "Kubctl" e la herramienta para intercatuar con los clústers de Kubernetes.

Se creara un clúster de Kubernetes con "Kind", utilizando la configuración de "KindConfig.yaml" y se configuran los despliegues de las aplicaciones de Drupal y MySql usando la herramienta "Kubctl".
```yaml
- task: HelmInstaller@0
  inputs:
    helmVersion: '2.14.1'
    installKubectl: true
  displayName: 'Instalar Kubernetes'

- script: |
    kind create cluster --config kindConfig.yaml
    kubectl apply -f drupalConfig.yaml
    kubectl apply -f mysqlConfig.yaml
  displayName: 'Despliegue Kubernetes'
```

## Analizar código con SonarQube
"SonarQubeAnalyze" se encarga de ejecutar el análisis estático de código y especificando la versión JDK a utilizar durante el análisis.
```yaml
- task: SonarQubeAnalyze@5
  inputs:
    jdkversion: 'JAVA_HOME_11_X64'
  displayName: 'Ejecutar sonar'
``` 

## Publicar resultados SonarQube
"SonarQubePublish" se encargará de publicar los resultados del análisis, estableciendo un tiempo de espera para la finalización del proyecto.
```yaml
- task: SonarQubePublish@5
  inputs:
    pollingTimeoutSec: '300'
  displayName: 'Publicar sonar'
```

## Pipeline
```yaml
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:
- task: SonarQubePrepare@5
  inputs:
    SonarQube: 'SonarK'
    scannerMode: 'CLI'
    configMode: 'manual'
    cliProjectKey: 'vsAzure_vsAzure_AYyld2zCyILi-MNuEvd5'
    cliProjectName: 'vsAzure'
    cliSources: '.'
  displayName: 'Preparando Sonar'

- task: HelmInstaller@0
  inputs:
    helmVersion: '2.14.1'
    installKubectl: true
  displayName: 'Instalar Kubernetes'

- script: |
    kind create cluster --config kindConfig.yaml
    kubectl apply -f drupalConfig.yaml
    kubectl apply -f mysqlConfig.yaml
  displayName: 'Despliegue Kubernetes'

- task: SonarQubeAnalyze@5
  inputs:
    jdkversion: 'JAVA_HOME_11_X64'
  displayName: 'Ejecutar sonar'

- task: SonarQubePublish@5
  inputs:
    pollingTimeoutSec: '300'
  displayName: 'Publicar sonar'
```

## Autores
-Rafael Leal Pardo
-Manuel Coca Alba

## Archvios
[Pipeline Ejercicio1](../Ejercicio1/azure-pipelines.yml)
[Pipeline Ejercicio2](../Ejercicio2/azure-pipelines.yml)
[Documento Pipeline Ejercicio2](../Ejercicio2/Documento.md)
[Pipeline Ejercicio3](../Ejercicio3/gitlab-ci.yml)
[Documento Pipeline Ejercicio3](../Ejercicio3/Documento.md)