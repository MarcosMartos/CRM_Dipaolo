from utils.csv_to_db import cargar_creditos, cargar_pagos, cargar_clientes
from app import app

if __name__ == "__main__":
    with app.app_context():
     
        cargar_clientes("data/clientes.csv")

        cargar_creditos("data/creditos.csv")

        cargar_pagos("data/pagos.csv")
