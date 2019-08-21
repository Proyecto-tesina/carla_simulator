# Uso:
Se recomienda usar un entorno virtual para la instalación de la librería PySide2 utilizada para la interfaz de la aplicación.
Para poder usar la aplicación se debe cumplir con:

- Tener corriendo el cliente de Carla. Donde se podrán instanciar los distintos actores de la simulación.
  (Opcionalmente se puede quitar la ventana de modo espectador del cliente previamente con `DISPLAY=`)
  ```bash
  bash CarlaEU4.sh
  ```
- Ejecutar el script para el control manual de un auto
  ```bash
  python driving_simulator.py
  ```
- Ejecutar la aplicación de publicidades
  ```bash
  python3 app.py
  ```
