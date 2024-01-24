import pandas as pd
import matplotlib.pyplot as plt

archivo_csv = 'SensorData.csv'
datos = pd.read_csv(archivo_csv)

columnas_seleccionadas = ['timestamp', 'temperatureSHT31', 'humiditySHT31']

for columna in columnas_seleccionadas[1:]:
    plt.plot(datos['timestamp'], datos[columna], label=columna, marker='o')

plt.title('Gráfico de Líneas - Temperatura y Humedad SHT31')
plt.xlabel('Timestamp')
plt.ylabel('Valor')
plt.legend()
plt.savefig('grafico.png')
plt.show()