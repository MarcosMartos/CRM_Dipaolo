from datetime import date, timedelta
from models import db, Cliente, Credito, Pago

def actualizar_estado_clientes():
    hoy = date.today()
    hace_un_ano = hoy - timedelta(days=365)

    clientes = Cliente.query.all()

    for cliente in clientes:
        creditos = Credito.query.filter(Credito.documento == cliente.documento).all()
        creditos_ids = [c.num_credito for c in creditos]

        # Promedio de créditos del último año
        creditos_recientes = [
            c for c in creditos if c.fecha_real and c.fecha_real >= hace_un_ano
        ]
        total_reciente = sum(c.total_facturado or 0 for c in creditos_recientes)
        promedio = total_reciente / len(creditos_recientes) if creditos_recientes else 0

        # Atrasos
        atrasos = Pago.query.filter(
            Pago.num_credito.in_(creditos_ids),
            Pago.vencimiento < hoy,
            Pago.importe_pago < Pago.importe
        ).count()

        # Estado
        if atrasos == 0:
            cliente.estado = "excelente" if promedio > 300_000 else "bueno"
        elif atrasos <= 2:
            cliente.estado = "remolon"
        else:
            cliente.estado = "malo"

    db.session.commit()
    print("✅ Estados de clientes actualizados.")
