from models import db, Credito, Pago, Cliente
from sqlalchemy import func
from datetime import date

# ====================== MÉTRICAS EXISTENTES ======================

def cantidad_creditos():
    return db.session.query(func.count(Credito.id)).scalar()

def importe_creditos():
    return db.session.query(func.sum(Credito.total_facturado)).scalar() or 0

def pagado_creditos():
    return db.session.query(func.sum(Pago.importe_pago)).scalar() or 0

def deuda_creditos():
    return importe_creditos() - pagado_creditos()

def creditos_atrasados():
    hoy = date.today()
    subq = db.session.query(Pago.num_credito).filter(
        Pago.vencimiento < hoy,
        Pago.importe_pago < Pago.importe
    ).distinct()
    return subq.count()

def importe_atrasado():
    hoy = date.today()
    atrasados = db.session.query(Pago).filter(
        Pago.vencimiento < hoy,
        Pago.importe_pago < Pago.importe
    )
    total = sum(p.importe - (p.importe_pago or 0) for p in atrasados)
    return total

def tasa_recuperacion():
    total = importe_creditos()
    pagado = pagado_creditos()
    return round((pagado / total) * 100, 2) if total else 0

# ====================== MÉTRICAS EXTENDIDAS ======================

# Clientes pagadores: sin deuda
def clientes_pagadores():
    clientes_con_deuda = db.session.query(Pago.num_credito).filter(
        Pago.importe_pago < Pago.importe
    ).distinct().subquery()

    total_clientes = db.session.query(func.count(Cliente.id)).scalar()
    clientes_con_deuda_count = db.session.query(Credito).filter(
        Credito.num_credito.in_(clientes_con_deuda)
    ).distinct().count()

    return total_clientes - clientes_con_deuda_count

# Clientes remolones: deuda leve (1-2 cuotas vencidas)
def clientes_remolones():
    hoy = date.today()

    subq = db.session.query(
        Pago.num_credito,
        func.count(Pago.id).label("cuotas_atrasadas")
    ).filter(
        Pago.vencimiento < hoy,
        Pago.importe_pago < Pago.importe
    ).group_by(Pago.num_credito).subquery()

    count = db.session.query(subq).filter(
        subq.c.cuotas_atrasadas.between(1, 2)
    ).count()

    return count

# Clientes malos: deuda grave (3+ cuotas vencidas)
def clientes_malos():
    hoy = date.today()

    subq = db.session.query(
        Pago.num_credito,
        func.count(Pago.id).label("cuotas_atrasadas")
    ).filter(
        Pago.vencimiento < hoy,
        Pago.importe_pago < Pago.importe
    ).group_by(Pago.num_credito).subquery()

    count = db.session.query(subq).filter(
        subq.c.cuotas_atrasadas >= 3
    ).count()

    return count

# Tasa de reincidencia (créditos que alguna vez estuvieron atrasados)
def tasa_reincidencia():
    total_creditos = db.session.query(func.count(Credito.id)).scalar()

    hoy = date.today()

    atrasados = db.session.query(Pago.num_credito).filter(
        Pago.vencimiento < hoy,
        Pago.importe_pago < Pago.importe
    ).distinct().count()

    return round((atrasados / total_creditos) * 100, 2) if total_creditos else 0
