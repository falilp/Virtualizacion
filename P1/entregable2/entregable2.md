# Configuración de Docker Compose para WordPress y MariaDB

Este archivo de Docker Compose se utiliza para orquestar la ejecución de dos servicios, WordPress y MariaDB, en contenedores Docker. A continuación, se describen las configuraciones realizadas en este archivo:

## Definición de la versión de la sintaxis de Docker Compose
```yaml
version: '3'
```

## Definición de redes
```yaml
networks:
  redDocker:
```

## Servicio para WordPress
```yaml
wordpress:
  image: wordpress:latest
  ports:
    - "82:80"
  networks:
    - redDocker
```
Se configura el servicio para WordPress. Aquí están los detalles:
- Se utiliza la imagen "wordpress:latest" como base para el contenedor de WordPress.
- Se mapea el puerto 82 del host al puerto 80 en el contenedor, permitiendo acceder a WordPress desde el puerto 82 del host.
- Se vincula la red "redDocker" al contenedor de WordPress. Esto permite que ambos contenedores se vean entre ellos.

## Servicio para MariaDB
```yaml
mariadb:
  image: mariadb:latest
  environment:
    MYSQL_DATABASE: wordpress
    MYSQL_ROOT_PASSWORD: root 
  networks:
    - redDocker
```
Se configura el servicio para MariaDB. Aquí están los detalles:
- Se utiliza la imagen "mariadb:latest" como base para el contenedor de MariaDB.
- Se establecen las variables de entorno para configurar MariaDB:
  - MYSQL_DATABASE se establece en "drupal" para crear una base de datos llamada "drupal".
  - MYSQL_ROOT_PASSWORD se establece en "root" como la contraseña del usuario root de MariaDB.
- Al igual que en el servicio de Drupal, se vincula el contenedor a la red "redDocker" para que pueda ver directamente al otro servicio.

## Resumen
Estas configuraciones permiten ejecutar WordPress y MariaDB en contenedores Docker de manera coordinada.