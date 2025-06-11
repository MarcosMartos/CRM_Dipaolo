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
# Nuevas métricas basadas en el campo 'estado' que ya está calculado

def clientes_excelentes():
    return db.session.query(func.count()).filter(Cliente.estado == 'excelente').scalar()

def clientes_buenos():
    return db.session.query(func.count()).filter(Cliente.estado == 'bueno').scalar()

def clientes_remolones():
    return db.session.query(func.count()).filter(Cliente.estado == 'remolon').scalar()

def clientes_malos():
    return db.session.query(func.count()).filter(Cliente.estado == 'malo').scalar()

def clientes_total():
    return db.session.query(func.count(Cliente.id)).scalar()


# Tasa de reincidencia (créditos que alguna vez estuvieron atrasados)
def tasa_reincidencia():
    total_creditos = db.session.query(func.count(Credito.id)).scalar()

    hoy = date.today()

    atrasados = db.session.query(Pago.num_credito).filter(
        Pago.vencimiento < hoy,
        Pago.importe_pago < Pago.importe
    ).distinct().count()

    return round((atrasados / total_creditos) * 100, 2) if total_creditos else 0
