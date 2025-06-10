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

# Carga de créditos optimizada
def cargar_creditos(ruta):
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    existentes = set(r[0] for r in db.session.query(Credito.num_credito).all())
    nuevos_creditos = []

    for _, row in df.iterrows():
        num_credito = to_int(row.get('NROCREDI'))
        if not num_credito or num_credito in existentes:
            continue

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
        nuevos_creditos.append(credito)

    if nuevos_creditos:
        db.session.bulk_save_objects(nuevos_creditos)
        db.session.commit()

# Carga de pagos optimizada
def cargar_pagos(ruta):
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    creditos_existentes = set(r[0] for r in db.session.query(Credito.num_credito).all())
    pagos_existentes = {(p.num_credito, p.num_cuota) for p in db.session.query(Pago.num_credito, Pago.num_cuota).all()}
    nuevos_pagos = []

    for _, row in df.iterrows():
        num_credito = to_int(row.get('num_credito'))
        num_cuota = to_int(row.get('num_cuota'))

        if not num_credito or not num_cuota:
            continue
        if num_credito not in creditos_existentes:
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
        nuevos_pagos.append(pago)

    if nuevos_pagos:
        db.session.bulk_save_objects(nuevos_pagos)
        db.session.commit()

# Carga de clientes (optimizada previamente)
def cargar_clientes(ruta):
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    nuevos_clientes = []

    # Obtener documentos únicos del archivo
    df['documento'] = df['documento'].astype(str).str.replace('.', '').str.strip()
    df = df.drop_duplicates(subset='documento')

    # Obtener documentos existentes en la DB
    documentos_existentes = {
        r[0] for r in db.session.query(Cliente.documento).all()
    }

    for _, row in df.iterrows():
        doc = str(row.get('documento')).strip()
        if not doc or doc in documentos_existentes:
            continue

        cliente = Cliente(
            apellido=limpiar(row.get('apellido'), ''),
            documento=doc,
            telefono=limpiar(row.get('telefono'), ''),
            domicilio=limpiar(row.get('domicilio'), ''),
            historial_atraso=to_int(row.get('historial_atraso'), 0),
            estado=limpiar(row.get('estado'), 'bueno')
        )
        nuevos_clientes.append(cliente)

    if nuevos_clientes:
        db.session.bulk_save_objects(nuevos_clientes)
        db.session.commit()

