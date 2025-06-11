from models import db, Credito, Pago, Cliente
from sqlalchemy import func
from datetime import date

# === MÉTRICAS GENERALES ===
def cantidad_creditos_totales():
    return db.session.query(func.count(Credito.id)).scalar()

def importe_total_creditos():
    return db.session.query(func.sum(Credito.total_facturado)).scalar() or 0

# === MÉTRICAS DE CRÉDITOS ACTIVOS ===
def creditos_activos():
    return db.session.query(Credito).filter(Credito.estado == "activo")

def cantidad_creditos_activos():
    return creditos_activos().count()

def importe_total_activos():
    return db.session.query(func.sum(Credito.total_facturado)).filter(Credito.estado == "activo").scalar() or 0

def pagado_total_activos():
    activos = db.session.query(Credito.num_credito).filter(Credito.estado == "activo").subquery()
    return db.session.query(func.sum(Pago.importe_pago)).filter(Pago.num_credito.in_(activos)).scalar() or 0

def deuda_total_activos():
    return importe_total_activos() - pagado_total_activos()

def porcentaje_pagado():
    total = importe_total_activos()
    pagado = pagado_total_activos()
    return round((pagado / total) * 100, 2) if total else 0

def porcentaje_deuda():
    total = importe_total_activos()
    deuda = deuda_total_activos()
    return round((deuda / total) * 100, 2) if total else 0

# === MÉTRICAS DE CLIENTES POR ESTADO ===
def total_clientes():
    return db.session.query(Cliente).count()

def contar_clientes_por_estado(estado):
    return db.session.query(Cliente).filter(Cliente.estado == estado).count()

def porcentaje_clientes(estado):
    total = total_clientes()
    cantidad = contar_clientes_por_estado(estado)
    return round((cantidad / total) * 100, 2) if total else 0
