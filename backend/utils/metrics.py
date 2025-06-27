from models import db, Cliente, Credito, Pago
from sqlalchemy import func, select
from datetime import date

# Esta función calcula diversas métricas financieras y operativas sobre los créditos otorgados y activos.
def get_credit_metrics():
    today = date.today()

    pagos_no_saldados = (
        db.session.query(Pago.num_credito)
        .filter(Pago.importe_pago < Pago.importe)
        .distinct()
        .subquery()
    )

    creditos_activos = (
        db.session.query(Credito)
        .filter(Credito.num_credito.in_(select(pagos_no_saldados)))
        .all()
    )

    creditos_activos_ids = [c.num_credito for c in creditos_activos]
    total_creditos_activos = len(creditos_activos)
    total_creditos_otorgados = db.session.query(Credito).count()
    importe_total_activos = sum(float(c.total_facturado or 0) for c in creditos_activos)

    pagos_activos = db.session.query(Pago).filter(Pago.num_credito.in_(creditos_activos_ids)).all()
    cuotas_totales = len(pagos_activos)
    cuotas_pagadas = [p for p in pagos_activos if p.fecha_pago]
    cuotas_no_pagadas = [p for p in pagos_activos if not p.fecha_pago]

    total_pagado = sum(float(p.importe_pago or 0) for p in cuotas_pagadas)
    total_deuda = sum(float(p.importe or 0) for p in cuotas_no_pagadas)

    atrasados = [p for p in cuotas_no_pagadas if p.vencimiento and p.vencimiento < today]
    creditos_con_atrasos = {p.num_credito for p in atrasados}
    total_atrasado = sum(float(p.importe or 0) for p in atrasados)

    porcentaje_cuotas_pagadas = (len(cuotas_pagadas) / cuotas_totales * 100) if cuotas_totales else 0
    porcentaje_cuotas_no_pagadas = (len(cuotas_no_pagadas) / cuotas_totales * 100) if cuotas_totales else 0
    porcentaje_pagado = (total_pagado / (total_pagado + total_deuda) * 100) if (total_pagado + total_deuda) else 0
    porcentaje_deuda = (total_deuda / (total_pagado + total_deuda) * 100) if (total_pagado + total_deuda) else 0
    porcentaje_atrasado = (len(creditos_con_atrasos) / total_creditos_activos * 100) if total_creditos_activos else 0

    return {
        'creditos_otorgados': total_creditos_otorgados,
        'creditos_activos': total_creditos_activos,
        'importe_total_creditos_activos': round(importe_total_activos, 2),
        'cuotas_totales_creditos_activos': cuotas_totales,
        'importe_pagado_creditos_activos': round(total_pagado, 2),
        'porcentaje_pagado_creditos_activos': round(porcentaje_pagado, 2),
        'porcentaje_cuotas_pagadas_creditos_activos': round(porcentaje_cuotas_pagadas, 2),
        'importe_deuda_creditos_activos': round(total_deuda, 2),
        'porcentaje_deuda_creditos_activos': round(porcentaje_deuda, 2),
        'porcentaje_cuotas_no_pagadas_creditos_activos': round(porcentaje_cuotas_no_pagadas, 2),
        'importe_atrasado_creditos_activos': round(total_atrasado, 2),
        'porcentaje_atrasado_creditos_activos': round(porcentaje_atrasado, 2),
    }

# Esta función calcula la cantidad y porcentaje de clientes agrupados por estado.
def get_client_metrics():
    total_clientes = db.session.query(func.count(Cliente.documento)).scalar()
    estados = db.session.query(Cliente.estado, func.count(Cliente.documento)).group_by(Cliente.estado).all()

    return {
        estado: {
            'cantidad': cant,
            'porcentaje': round((cant / total_clientes) * 100, 2) if total_clientes else 0
        }
        for estado, cant in estados
    }
