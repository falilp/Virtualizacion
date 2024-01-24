# Manuel Coca Alba y Rafael Leal Pardo: Despliegue de aplicaciones en Kubernetes

# Documentación de Configuración

## kindConfig.yaml

Este archivo de configuración de Kubernetes se utiliza para orquestar la ejecución de un clúster con Kind. A continuación, se describen las configuraciones realizadas en este archivo:

```yaml
#Se define el tipo de recurso - Cluster 
kind: Cluster

#Se especifica la versión de la API de Kind
apiVersion: kind.x-k8s.io/v1alpha4

#Se define el nodo en el Cluster, el cual tiene el role de control-plane
nodes:
- role: control-plane

#Se mapea para el nodo, en el puerto 30080 del contendor
#se mapeará al puerto 8085 utilizando el protocolo TCP
  extraPortMappings:
  - containerPort: 30080
    hostPort: 8085
    protocol: TCP
```

Su configuración es la siguiente:
- Se configura el tipo de recurso como `Cluster` y se utiliza la versión `v1alpha4` de la API de Kind.
- Se define un nodo en el clúster con el rol de `control-plane`, que es el nodo principal que controla el clúster.
- Se define un mapeo de puerto extra para el nodo. Esto significa que el puerto `30080` del contenedor se mapeará al puerto `8085` del host, utilizando el protocolo `TCP`.

## drupalConfig.yaml

Este archivo de configuración de Kubernetes se utiliza para orquestar la ejecución de dos servicios, Drupal y MySQL, en contenedores. A continuación, se describen las configuraciones realizadas en este archivo:

### Definición de la implementación de Drupal

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: drupal
  
#Se especifican las características de la implementación.
spec:
  replicas: 2 #Indica el numero de replicas

#Se define el selector de la implementación.
  selector:
    matchLabels:
      app: drupal

#Se define la plantilla de la implementación.
  template:
    metadata:
      labels:
        app: drupal

#Características de la plantilla.
    spec:
      containers:
        - name: drupal
          image: drupal:latest #La imagen del contenedor.
          ports:
            - containerPort: 80 #El puerto del contenedor.

#Se definen los montajes de volumen del contenedor.
          volumeMounts:
          - name: drupalpersistentstorage 
            mountPath: /drupal 

#Se definen los volúmenes de la plantilla.
      volumes: 
        - name: drupalpersistentstorage 
          persistentVolumeClaim: #La reclamación del volumen persistente.
            claimName: drupalpvcclaim 
````

Se configura la implementación para Drupal. Aquí están los detalles:
- Se utiliza la imagen "drupal:latest" como base para el contenedor de Drupal.
- Se configuran dos réplicas para la implementación.
- Se mapea el puerto 80 del contenedor, permitiendo acceder a Drupal desde este puerto.
- Se monta un volumen persistente en la ruta `/drupal` del contenedor.

### Definición del servicio de Drupal

````yaml
apiVersion: v1
kind: Service
metadata:
  name: drupal

#Se especifican las características del servicio.
spec:
  type: NodePort #El tipo de servicio. NodePort permite acceder al servicio desde fuera del clúster.
  
#Se definen los puertos del servicio.  
  ports:
    - name: http
      port: 80 #El puerto del servicio
      nodePort: 30080 #El puerto del nodo al que se mapeará el puerto del servicio.
  selector:
    app: drupal
````

Se configura el servicio para Drupal. Aquí están los detalles:
- Se configura el tipo de servicio como `NodePort`, lo que permite acceder al servicio desde fuera del clúster.
- Se mapea el puerto 30080 del nodo al puerto 80 del servicio, permitiendo acceder a Drupal desde el puerto 30080 del nodo.

### Definición de la reclamación del volumen persistente de Drupal

````yaml
apiVersion: v1
kind: PersistentVolumeClaim 
metadata:
  name: drupalpvcclaim 

#Se especifican las características de la reclamación del volumen persistente.
spec:
  accessModes:
    - ReadWriteOnce #El modo de acceso. ReadWriteOnce permite que el volumen sea leído y escrito por un único nodo.

#Se definen los recursos de la reclamación del volumen persistente.  
  resources:
    requests:
      storage: 256Mi #La cantidad de almacenamiento solicitada para el volumen.
````

Se configura la reclamación del volumen persistente para Drupal. Aquí están los detalles:
- Se configura el modo de acceso como `ReadWriteOnce`, lo que permite que el volumen sea leído y escrito por un único nodo.
- Se solicita un almacenamiento de 256Mi para el volumen.

## mysqlConfig.yaml

Este archivo de configuración de Kubernetes se utiliza para orquestar la ejecución del servicio MySQL en un contenedor. A continuación, se describen las configuraciones realizadas en este archivo:

### Definición de la implementación de MySQL

````yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql

#Se especifican las características de la implementación.
spec:
  replicas: 1 #Indica el numero de replicas

#Se define el selector de la implementación.
  selector:
    matchLabels:
      app: mysql

#Se define la plantilla de la implementación.
  template:
    metadata:
      labels:
        app: mysql

#Características de la plantilla.
    spec:
      containers:
        - name: mysql
          image: mysql:latest #La imagen del contenedor.
          ports:
            - containerPort: 3306 #El puerto del contenedor.

#Se definen las variables de entorno del contenedor.
          env:
          - name: MYSQL_HOST
            value: 'localhost'
          - name: MYSQL_ALLOW_EMPTY_PASSWORD
            value: 'yes'
          - name: MYSQL_DATABASE
            value: 'VS'

#Se definen los montajes de volumen del contenedor.
          volumeMounts:
          - name: mysqlpersistentstorage 
            mountPath: /mysql

#Se definen los volúmenes de la plantilla. 
      volumes: 
        - name: mysqlpersistentstorage 
          persistentVolumeClaim: #La reclamación del volumen persistente.
            claimName: mysqlpvcclaim  
````

Se configura la implementación para MySQL. Aquí están los detalles:
- Se utiliza la imagen "mysql:latest" como base para el contenedor de MySQL.
- Se configura una réplica para la implementación.
- Se mapea el puerto 3306 del contenedor, permitiendo acceder a MySQL desde este puerto.
- Se establecen las variables de entorno para configurar MySQL:
  - MYSQL_HOST se establece en "localhost".
  - MYSQL_ALLOW_EMPTY_PASSWORD se establece en "yes" para permitir una contraseña vacía.
  - MYSQL_DATABASE se establece en "VS" para crear una base de datos llamada "VS".
- Se monta un volumen persistente en la ruta `/mysql` del contenedor.

### Definición del servicio de MySQL

````yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql

#Se especifican las características del servicio.
spec:
  type: ClusterIP #El tipo de servicio. ClusterIP permite acceder al servicio desde dentro del clúster.

#Se define el selector del servicio.  
  selector:
    app: mysql

#Se definen los puertos del servicio.
  ports:
    - name: http
      port: 3306 #El puerto del servicio.
      targetPort: 3306 #El puerto del contenedor al que se mapeará el puerto del servicio.
````

Se configura el servicio para MySQL. Aquí están los detalles:
- Se configura el tipo de servicio como `ClusterIP`, lo que permite acceder al servicio desde dentro del clúster.
- Se mapea el puerto 3306 del servicio al mismo puerto del contenedor, permitiendo acceder a MySQL desde este puerto.

### Definición de la reclamación del volumen persistente de MySQL

````yaml
apiVersion: v1
kind: PersistentVolumeClaim 
metadata:
  name: mysqlpvcclaim 

#Se especifican las características de la reclamación del volumen persistente.
spec:
  accessModes:
    - ReadWriteOnce #El modo de acceso. ReadWriteOnce permite que el volumen sea leído y escrito por un único nodo.

#Se definen los recursos de la reclamación del volumen persistente.  
  resources:
    requests:
      storage: 256Mi 
````

Se configura la reclamación del volumen persistente para MySQL. Aquí están los detalles:
- Se configura el modo de acceso como `ReadWriteOnce`, lo que permite que el volumen sea leído y escrito por un único nodo.
- Se solicita un almacenamiento de 256Mi para el volumen.