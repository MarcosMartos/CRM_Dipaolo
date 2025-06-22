import logging
from flask import Blueprint, request
from app.extensions import db
from app.models import Cliente, Credito, Pago
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import tuple_

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/cargar_datos", methods=["POST"])
def cargar_datos():
    try:
        archivo_clientes = request.files['archivo_clientes']
        archivo_creditos = request.files['archivo_creditos']
        archivo_pagos = request.files['archivo_pagos']

        logging.info("Iniciando carga de clientes...")
        df_clientes = pd.read_excel(archivo_clientes)
        df_clientes = df_clientes.drop_duplicates(subset=['documento'])

        stmt_clientes = insert(Cliente).values([
            {
                'apellido': row['apellido'],
                'documento': row['documento'],
                'telefono': row['telefono'],
                'domicilio': row['domicilio'],
                'historial_atraso': row['historial_atraso'],
                'estado': row['estado']
            } for _, row in df_clientes.iterrows()
        ])
        stmt_clientes = stmt_clientes.on_conflict_do_nothing(index_elements=['documento'])
        db.session.execute(stmt_clientes)
        db.session.commit()
    except Exception as e:
        logging.error(f"Error al cargar clientes: {e}")
        db.session.rollback()

    try:
        logging.info("Iniciando carga de créditos...")
        df_creditos = pd.read_excel(archivo_creditos)

        df_creditos = df_creditos.astype({'num_credito': int, 'documento': str})
        creditos_existentes = db.session.query(Credito.num_credito).filter(
            Credito.num_credito.in_(df_creditos['num_credito'].tolist())
        ).all()
        creditos_existentes = set(row[0] for row in creditos_existentes)

        nuevos_creditos = [
            {
                'num_credito': int(row['num_credito']),
                'documento': row['documento'],
                'monto': row['monto'],
                'cuotas': row['cuotas'],
                'estado': row['estado']
            }
            for _, row in df_creditos.iterrows()
            if int(row['num_credito']) not in creditos_existentes
        ]

        if nuevos_creditos:
            db.session.bulk_insert_mappings(Credito, nuevos_creditos)
            db.session.commit()
    except Exception as e:
        logging.error(f"Error al cargar créditos: {e}")
        db.session.rollback()

    try:
        logging.info("Iniciando carga de pagos...")
        df_pagos = pd.read_excel(archivo_pagos)

        df_pagos = df_pagos.astype({'num_credito': int, 'cuota': int})
        pagos_existentes = db.session.query(Pago.num_credito, Pago.cuota).filter(
            tuple_(Pago.num_credito, Pago.cuota).in_([
                (int(row['num_credito']), int(row['cuota'])) for _, row in df_pagos.iterrows()
            ])
        ).all()
        pagos_existentes = set(pagos_existentes)

        nuevos_pagos = [
            {
                'num_credito': int(row['num_credito']),
                'cuota': int(row['cuota']),
                'monto_pagado': row['monto_pagado'],
                'fecha_pago': row['fecha_pago']
            }
            for _, row in df_pagos.iterrows()
            if (int(row['num_credito']), int(row['cuota'])) not in pagos_existentes
        ]

        if nuevos_pagos:
            db.session.bulk_insert_mappings(Pago, nuevos_pagos)
            db.session.commit()
    except Exception as e:
        logging.error(f"Error al cargar pagos: {e}")
        db.session.rollback()

    logging.info("Carga completada.")
    return "Datos cargados correctamente", 202
