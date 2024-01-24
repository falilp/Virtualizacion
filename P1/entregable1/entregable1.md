# Configuración de Docker Compose para Drupal y MySQL

Este archivo de Docker Compose se utiliza para orquestar la ejecución de dos servicios, Drupal y MySQL, en contenedores Docker. A continuación, se describen las configuraciones realizadas en este archivo:

## Definición de la versión de la sintaxis de Docker Compose
```yaml
version: '3'
```

## Definición de volúmenes
```yaml
volumes:
  volumenDocker:
```

## Servicio para Drupal
```yaml
drupal:
  image: drupal:latest
  ports:
    - "81:80"
  volumes:
    - volumenDocker:/shared
```
Se configura el servicio para Drupal. Aquí están los detalles:
- Se utiliza la imagen "drupal:latest" como base para el contenedor de Drupal.
- Se mapea el puerto 81 del host al puerto 80 en el contenedor, permitiendo acceder a Drupal desde el puerto 81 del host.
- Se vincula el volumen "volumenDocker" al directorio "/shared" en el contenedor de Drupal. Esto permite que Drupal almacene datos y configuraciones en el volumen, lo que garantiza la persistencia de los datos incluso si el contenedor se detiene o elimina.

## Servicio para MySQL
```yaml
mysql:
  image: mysql:latest
  environment:
    MYSQL_DATABASE: drupal
    MYSQL_ROOT_PASSWORD: root
  volumes:
    - volumenDocker:/shared
```
Se configura el servicio para MySQL. Aquí están los detalles:
- Se utiliza la imagen "mysql:latest" como base para el contenedor de MySQL.
- Se establecen las variables de entorno para configurar MySQL:
    - MYSQL_DATABASE se establece en "drupal" para crear una base de datos llamada "drupal".
    - MYSQL_ROOT_PASSWORD se establece en "root" como la contraseña del usuario root de MySQL.
- Al igual que en el servicio de Drupal, se vincula el volumen "volumenDocker" al directorio "/shared" en el contenedor de MySQL para garantizar la persistencia de los datos de la base de datos.

## Resumen
Estas configuraciones permiten ejecutar Drupal y MySQL en contenedores Docker de manera coordinada y aseguran que los datos se mantengan persistentes a través del uso de volúmenes.