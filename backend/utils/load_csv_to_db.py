import os
import pandas as pd
from datetime import datetime
from models import db, Cliente, Credito, Pago
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import tuple_

DATA_FOLDER = "data"
BATCH_SIZE = 1000

def parse_date(value):
    try:
        parsed = pd.to_datetime(value, dayfirst=True, errors='coerce')
        return parsed.date() if pd.notna(parsed) else None
    except Exception:
        return None

def safe_int(value):
    try:
        return int(str(value).replace('.', '').replace(',', '').strip())
    except:
        return None

def safe_float(value):
    try:
        return float(str(value).replace(',', '.').strip())
    except:
        return None

def safe_str(value):
    try:
        return str(value).strip() if pd.notna(value) else None
    except:
        return None

def calcular_estado_cliente(documento):
    creditos = Credito.query.filter_by(documento=documento).all()
    pagos = Pago.query.filter(Pago.num_credito.in_([c.num_credito for c in creditos])).all()

    atrasos = 0
    for p in pagos:
        if not p.fecha_pago or (p.importe_pago is not None and p.importe_pago < p.importe):
            atrasos += 1

    monto_total = sum(c.total_facturado for c in creditos if c.fecha_real and c.fecha_real.year >= pd.Timestamp.today().year - 1)

    if atrasos > 2:
        return "malo"
    elif atrasos == 1:
        return "remolon"
    elif monto_total > 1000000:
        return "excelente"
    else:
        return "bueno"

def cargar_todos_los_datos():
    documentos_modificados = set()

    # Cargar clientes
    try:
        df_clientes = pd.read_csv(os.path.join(DATA_FOLDER, "clientes.csv"))
        df_clientes.dropna(subset=['documento'], inplace=True)
        df_clientes = df_clientes[df_clientes['documento'].astype(str).str.strip() != '']

        for start in range(0, len(df_clientes), BATCH_SIZE):
            batch = df_clientes.iloc[start:start + BATCH_SIZE]
            stmt = insert(Cliente).values([{
                'apellido': safe_str(row['apellido']),
                'documento': safe_str(row['documento']),
                'telefono': safe_str(row['telefono']),
                'domicilio': safe_str(row['domicilio']),
                'estado': 'pendiente'
            } for _, row in batch.iterrows()])
            stmt = stmt.on_conflict_do_update(
                index_elements=['documento'],
                set_={
                    'apellido': stmt.excluded.apellido,
                    'telefono': stmt.excluded.telefono,
                    'domicilio': stmt.excluded.domicilio
                }
            )
            db.session.execute(stmt)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Error cargando clientes: {e}", 500

    # Cargar créditos
    try:
        df_creditos = pd.read_csv(os.path.join(DATA_FOLDER, "creditos.csv"))
        df_creditos.dropna(subset=['num_credito', 'documento'], inplace=True)
        df_creditos = df_creditos[df_creditos['documento'].astype(str).str.strip() != '']

        for start in range(0, len(df_creditos), BATCH_SIZE):
            batch = df_creditos.iloc[start:start + BATCH_SIZE]
            for _, row in batch.iterrows():
                values = {
                    'num_credito': safe_int(row['num_credito']),
                    'documento': safe_str(row['documento']),
                    'num_factura': safe_int(row['num_factura']),
                    'total_facturado': safe_float(row['total_facturado']),
                    'anticipo': safe_float(row.get('anticipo')),
                    'financiacion': safe_float(row.get('financiacion')),
                    'num_cuotas': safe_int(row['num_cuotas']),
                    'vto_primer_cuota': parse_date(row['vto_primer_cuota']),
                    'fecha_real': parse_date(row['fecha_real']),
                    'sucursal': safe_int(row['sucursal']),
                    'vendedor': safe_int(row['vendedor']),
                    'articulo_1': safe_int(row.get('articulo_1')),
                    'cantidad_1': safe_int(row.get('cantidad_1')),
                    'articulo_2': safe_int(row.get('articulo_2')),
                    'cantidad_2': safe_int(row.get('cantidad_2')),
                    'articulo_3': safe_int(row.get('articulo_3')),
                    'cantidad_3': safe_int(row.get('cantidad_3')),
                    'articulo_4': safe_int(row.get('articulo_4')),
                    'cantidad_4': safe_int(row.get('cantidad_4')),
                    'articulo_5': safe_int(row.get('articulo_5')),
                    'cantidad_5': safe_int(row.get('cantidad_5')),
                    'articulo_6': safe_int(row.get('articulo_6')),
                    'cantidad_6': safe_int(row.get('cantidad_6')),
                    'articulo_7': safe_int(row.get('articulo_7')),
                    'cantidad_7': safe_int(row.get('cantidad_7')),
                    'garante': safe_str(row.get('garante')),
                    'domicilio_garante': safe_str(row.get('domicilio_garante'))
                }
                stmt = insert(Credito).values(values)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['num_credito'],
                    set_=values
                )
                db.session.execute(stmt)
                documentos_modificados.add(values['documento'])
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Error cargando creditos: {e}", 500

    # Cargar pagos
    try:
        df_pagos = pd.read_csv(os.path.join(DATA_FOLDER, "pagos.csv"))
        df_pagos.dropna(subset=['num_credito', 'num_cuota'], inplace=True)

        creditos_existentes = set(
            c[0] for c in db.session.query(Credito.num_credito).filter(
                Credito.num_credito.in_([safe_int(x) for x in df_pagos['num_credito'].unique()])
            ).all()
        )

        for start in range(0, len(df_pagos), BATCH_SIZE):
            batch = df_pagos.iloc[start:start + BATCH_SIZE]
            for _, row in batch.iterrows():
                key = (safe_int(row['num_credito']), safe_int(row['num_cuota']))
                if key[0] not in creditos_existentes:
                    continue
                values = {
                    'num_credito': key[0],
                    'num_cuota': key[1],
                    'vencimiento': parse_date(row['vencimiento']),
                    'fecha_pago': parse_date(row['fecha_pago']),
                    'importe': safe_float(row['importe']),
                    'importe_pago': safe_float(row['importe_pago']),
                    'vendedor': safe_int(row['vendedor'])
                }
                stmt = insert(Pago).values(values)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['num_credito', 'num_cuota'],
                    set_=values
                )
                db.session.execute(stmt)
                credito = Credito.query.get(key[0])
                if credito:
                    documentos_modificados.add(credito.documento)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Error cargando pagos: {e}", 500

    # Actualizar estado de los clientes
    for documento in documentos_modificados:
        cliente = Cliente.query.filter_by(documento=documento).first()
        if cliente:
            cliente.estado = calcular_estado_cliente(documento)
    db.session.commit()

    return "Carga y actualización completadas", 200
