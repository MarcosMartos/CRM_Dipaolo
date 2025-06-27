from models import db

class Pago(db.Model):
    __tablename__ = 'pagos'
    __table_args__ = (
        db.UniqueConstraint('num_credito', 'num_cuota', name='unique_pago_credito_cuota'),
    )

    id = db.Column(db.Integer, primary_key=True)
    num_credito = db.Column(db.Integer, db.ForeignKey('creditos.num_credito'), nullable=False)
    num_cuota = db.Column(db.Integer)
    vencimiento = db.Column(db.Date)
    fecha_pago = db.Column(db.Date)
    importe = db.Column(db.Float)
    importe_pago = db.Column(db.Float)
    vendedor = db.Column(db.Integer)

