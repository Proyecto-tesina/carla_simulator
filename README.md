# Uso:
Se recomienda usar un entorno virtual para la instalación de las dependencias utilizadas en requirements.txt
Para poder usar la aplicación se debe cumplir con:

- Descargar el cliente de Carala (actualmente en la versión 0.9.6) del siguiente [link](https://github.com/carla-simulator/carla/blob/master/Docs/download.md) y extraer la carpeta en el directorio base con el nombre `Carla`
- Clonar este repositorio en el mismo directorio base
- Tener corriendo el cliente de Carla. Donde se podrán instanciar los distintos actores de la simulación.
  (Opcionalmente se puede quitar la ventana de modo espectador del cliente previamente con `DISPLAY=`)
  ```bash
  bash CarlaEU4.sh
  ```
- Ejecutar el script para el control manual de un auto
  ```bash
  python3 simulador/driving_simulator.py
  ```
- Ejecutar la aplicación de publicidades
  ```bash
  python3 app.py
  ```
