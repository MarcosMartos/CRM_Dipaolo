# backend/cargar_todo.py
import os
import time
import logging
from app import app

logging.basicConfig(filename='carga_datos.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def cargar_todo():
    from utils.csv_to_db import cargar_clientes, cargar_creditos, cargar_pagos

    base_path = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(base_path, "data")

    with app.app_context():
        inicio = time.time()

        try:
            path = os.path.join(data_dir, "clientes.csv")
            logging.info("Iniciando carga de clientes...")
            cargar_clientes(path)
        except Exception as e:
            logging.error(f"Error al cargar clientes: {e}")

        try:
            path = os.path.join(data_dir, "creditos.csv")
            logging.info("Iniciando carga de créditos...")
            cargar_creditos(path)
        except Exception as e:
            logging.error(f"Error al cargar créditos: {e}")

        try:
            path = os.path.join(data_dir, "pagos.csv")
            logging.info("Iniciando carga de pagos...")
            cargar_pagos(path)
        except Exception as e:
            logging.error(f"Error al cargar pagos: {e}")

        duracion = round(time.time() - inicio, 2)
        logging.info(f"Carga completada en {duracion} segundos.")
