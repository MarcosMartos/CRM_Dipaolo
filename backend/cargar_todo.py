# backend/cargar_todo.py
import os
import time
import logging
from app import app
from utils.load_csv_to_db import cargar_todos_los_datos

logging.basicConfig(
    filename='carga_datos.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def cargar_todo():
    with app.app_context():
        inicio = time.time()
        try:
            mensaje, status = cargar_todos_los_datos()
            if status == 200:
                logging.info("Datos cargados correctamente")
            else:
                logging.error(f"Error al cargar datos: {mensaje}")
        except Exception as e:
            logging.error(f"Error al ejecutar carga: {e}")

        duracion = round(time.time() - inicio, 2)
        logging.info(f"Carga completada en {duracion} segundos.")
