import pandas as pd
from models import db, Credito, Pago, Cliente
from datetime import datetime

# Función general de limpieza
def limpiar(valor, default=None):
    if pd.isna(valor) or valor is None:
        return default
    return str(valor).strip()

# Limpieza para documentos (quita puntos, espacios, etc.)
def limpiar_documento(valor, default=None):
    if pd.isna(valor) or valor is None:
        return default
    return str(valor).replace(".", "").replace(" ", "").strip()

# Conversión segura a entero
def to_int(valor, default=None):
    try:
        if pd.isna(valor) or valor is None or valor == '':
            return default
        return int(float(valor))
    except:
        return default

# Conversión segura de fechas
def parse_fecha(fecha):
    try:
        if pd.isna(fecha) or not fecha:
            return None
        fecha_str = str(int(float(fecha)))
        return datetime.strptime(fecha_str, "%Y%m%d").date()
    except:
        try:
            return datetime.strptime(str(fecha), "%Y-%m-%d").date()
        except:
            return None

# Carga de créditos
def cargar_creditos(ruta):
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    for _, row in df.iterrows():
        num_credito = to_int(row.get('NROCREDI'))
        if not num_credito:
            continue

        if not Credito.query.filter_by(num_credito=num_credito).first():
            credito = Credito(
                num_credito=num_credito,
                apellido=limpiar(row.get('APELLIDO'), ''),
                domicilio=limpiar(row.get('DOMICILIO'), ''),
                telefono=limpiar(row.get('TELEFONO'), ''),
                documento=limpiar(row.get('DOCUMENTO'), ''),
                vendedor=to_int(row.get('VENDEDOR')),
                sucursal=to_int(row.get('SUCURSAL')),
                num_factura=to_int(row.get('NROFACT')),
                total_facturado=to_int(row.get('TOTFACT')),
                fecha_real=parse_fecha(row.get('FECHREAL')),
                anticipo=to_int(row.get('ANTICIPO')),
                financiacion=to_int(row.get('FINANCIA')),
                num_cuotas=to_int(row.get('CUOTAS')),
                vto_primer_cuota=parse_fecha(row.get('VTO1RA')),
                artic1=limpiar(row.get('ARTIC1'), ''),
                cant1=to_int(row.get('CANT1')),
                artic2=limpiar(row.get('ARTIC2'), ''),
                cant2=to_int(row.get('CANT2')),
                artic3=limpiar(row.get('ARTIC3'), ''),
                cant3=to_int(row.get('CANT3')),
                artic4=limpiar(row.get('ARTIC4'), ''),
                cant4=to_int(row.get('CANT4')),
                artic5=limpiar(row.get('ARTIC5'), ''),
                cant5=to_int(row.get('CANT5')),
                artic6=limpiar(row.get('ARTIC6'), ''),
                cant6=to_int(row.get('CANT6')),
                artic7=limpiar(row.get('ARTIC7'), ''),
                cant7=to_int(row.get('CANT7')),
                garante=limpiar(row.get('GARANTE'), ''),
                dom_garante=limpiar(row.get('DOMGARAN'), ''),
                estado=limpiar(row.get('estado'), 'activo')
            )
            db.session.add(credito)
    db.session.commit()

# Carga de pagos
def cargar_pagos(ruta):
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    descartados = 0
    cargados = 0
    errores = []

    try:
        creditos_existentes = {c.num_credito for c in Credito.query.all()}
        pagos_existentes = {(p.num_credito, p.num_cuota) for p in Pago.query.all()}

        for _, row in df.iterrows():
            try:
                num_credito = to_int(row.get('num_credito'))
                num_cuota = to_int(row.get('num_cuota'))

                if not num_credito or not num_cuota:
                    descartados += 1
                    continue

                if num_credito not in creditos_existentes:
                    descartados += 1
                    continue

                if (num_credito, num_cuota) in pagos_existentes:
                    continue

                pago = Pago(
                    num_credito=num_credito,
                    num_cuota=num_cuota,
                    vencimiento=parse_fecha(row.get('vencimiento')),
                    fecha_pago=parse_fecha(row.get('fecha_pago')),
                    importe=float(limpiar(row.get('importe'), 0)),
                    importe_pago=float(limpiar(row.get('importe_pago'), 0)),
                    vendedor=to_int(row.get('vendedor'))
                )
                db.session.add(pago)
                cargados += 1

                if cargados % 100 == 0:
                    db.session.commit()

            except Exception as e:
                errores.append(f"Error en pago {num_credito} cuota {num_cuota}: {str(e)}")
                descartados += 1
                continue

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise

# Carga de clientes
def cargar_clientes(ruta):
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    for _, row in df.iterrows():
        doc = limpiar_documento(row.get('documento'))

        if not doc:
            continue

        if not Cliente.query.filter_by(documento=doc).first():
            cliente = Cliente(
                apellido=limpiar_documento(row.get('apellido'), ''),
                documento=doc,
                telefono=limpiar_documento(row.get('telefono'), ''),
                domicilio=limpiar_documento(row.get('domicilio'), ''),
                historial_atraso=to_int(row.get('historial_atraso'), 0)
            )
            db.session.add(cliente)
    db.session.commit()
