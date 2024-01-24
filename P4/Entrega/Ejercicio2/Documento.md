# Ejercicio 2 - Azure Pipeline Terraform
En Azure, un "pipeline" se refiere a Azure Pipelines, un servicio que automatiza la integración continua y entrega continua (CI/CD). Un pipeline en Azure Pipelines está definido por un archivo YAML o configurado visualmente, y consiste en trabajos y pasos que realizan tareas como compilación, prueba y despliegue. Los agentes ejecutan estos trabajos, y los pipelines pueden desencadenarse por eventos como cambios de código. Azure Pipelines proporciona flexibilidad para gestionar entornos y es esencial para automatizar el desarrollo, pruebas y despliegue de aplicaciones en Azure y otras plataformas.
## Preparación
Para poder realizar el pipeline debemos obtener primero nuestro repositorio en Azure para poder crear en los archivos necesarios de configuración además del pipeline, es necesario configurar SonarQube para que funcione con nuestro repositorio, para ello necesitaremos crear un servicio y crear una máquina virtual en Azure para luego realizar la instalación de SonarQube y su posterior configuración.

Debemos obtener el "cliProjectKey" y "cliProjectName" que debemos de crear con la ayuda de SonarQube para poder ejecutar el mismo en nuestro pipeline.

El archivo necesario para poder ejecutar el pipeline debemos utilizar el archivo main.tf de la práctica 2 de Azure.

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
    cliProjectKey: 'vsTerraform_vsTerraform_AYyqluuL6MiTmyf4G02t'
    cliProjectName: 'vsTerraform'
    cliSources: '.'
  displayName: 'Preparando Sonar'
```

## Instalar SDK de .NET
Esta tarea asegura que el entorno de ejecución en el agente de compilación tenga instalada la versión específica del SDK de .NET Core (3.1.x) necesaria para compilar y ejecutar aplicaciones .NET Core durante el resto del pipeline. Esto garantiza que las dependencias de .NET estén correctamente configuradas antes de proceder con otras tareas relacionadas con .NET en el pipeline.
```yaml
- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: '3.1.x'
    installationPath: $(Agent.ToolsDirectory)/dotnet
```

## Iniciar Terraform
Inicialización (terraform init): Prepara el entorno y descarga los proveedores necesarios.

Validación (terraform validate): Verifica la sintaxis y validez semántica de los archivos de configuración.

Ambas acciones son esenciales antes de aplicar cambios a la infraestructura para asegurarse de que la configuración esté correctamente definida y cumpla con los requisitos de Terraform.
```yaml
- script: |
    terraform init
    terraform validate
  displayName: 'Terraform Init and Validate'
```

## Ejecución Terraform
El pipeline ejecuta un comando Terraform para generar un plan detallado de los cambios propuestos en la infraestructura y guarda ese plan en un archivo llamado tfplan. El plan proporciona una vista previa de las acciones que Terraform tomará al aplicar los cambios, lo que permite una revisión manual antes de aplicarlos.
```yaml
- script: 'terraform plan -out=tfplan'
  displayName: 'Terraform Plan'
```

## Aplica Terraform
Esta parte del pipeline ejecuta el comando Terraform para aplicar los cambios planificados a la infraestructura. La opción -auto-approve evita que Terraform solicite confirmación manual, permitiendo que el proceso de aplicación sea totalmente automatizado.
```yaml
- script: 'terraform apply -auto-approve tfplan'
  displayName: 'Terraform Apply'
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
- master

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: SonarQubePrepare@5
  inputs:
    SonarQube: 'SonarK'
    scannerMode: 'CLI'
    configMode: 'manual'
    cliProjectKey: 'vsTerraform_vsTerraform_AYyqluuL6MiTmyf4G02t'
    cliProjectName: 'vsTerraform'
    cliSources: '.'
  displayName: 'Preparando Sonar'

- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: '3.1.x'
    installationPath: $(Agent.ToolsDirectory)/dotnet

- script: |
    terraform init
    terraform validate
  displayName: 'Terraform Init and Validate'

- script: 'terraform plan -out=tfplan'
  displayName: 'Terraform Plan'

- script: 'terraform apply -auto-approve tfplan'
  displayName: 'Terraform Apply'

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
[Documento Pipeline Ejercicio1](../Ejercicio1/Documento.md)
[Pipeline Ejercicio2](../Ejercicio2/azure-pipelines.yml)
[Pipeline Ejercicio3](../Ejercicio3/gitlab-ci.yml)
[Documento Pipeline Ejercicio3](../Ejercicio3/Documento.md)