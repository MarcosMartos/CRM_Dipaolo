from models import db

class Credito(db.Model):
    __tablename__ = 'creditos'

    num_credito = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(20), db.ForeignKey('clientes.documento'), nullable=False)
    vendedor = db.Column(db.Integer)
    sucursal = db.Column(db.Integer)
    num_factura = db.Column(db.Integer)
    fecha_real = db.Column(db.Date)
    total_facturado = db.Column(db.Float)
    anticipo = db.Column(db.Float)
    financiacion = db.Column(db.Float)
    num_cuotas = db.Column(db.Integer)
    vto_primer_cuota = db.Column(db.Date)
    articulo_1 = db.Column(db.Integer)
    cantidad_1 = db.Column(db.Integer)
    articulo_2 = db.Column(db.Integer)
    cantidad_2 = db.Column(db.Integer)
    articulo_3 = db.Column(db.Integer)
    cantidad_3 = db.Column(db.Integer)
    articulo_4 = db.Column(db.Integer)
    cantidad_4 = db.Column(db.Integer)
    articulo_5 = db.Column(db.Integer)
    cantidad_5 = db.Column(db.Integer)
    articulo_6 = db.Column(db.Integer)
    cantidad_6 = db.Column(db.Integer)
    articulo_7 = db.Column(db.Integer)
    cantidad_7 = db.Column(db.Integer)
    garante = db.Column(db.String(100))
    domicilio_garante = db.Column(db.String(150))

    pagos = db.relationship('Pago', backref='credito', lazy=True)
