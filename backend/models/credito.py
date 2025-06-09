from models import db

class Credito(db.Model):
    __tablename__ = 'creditos'

    id = db.Column(db.Integer, primary_key=True)
    num_credito = db.Column(db.BigInteger, unique=True, nullable=False)  # puede ser grande
    apellido = db.Column(db.String)
    domicilio = db.Column(db.String)
    telefono = db.Column(db.String)
    documento = db.Column(db.String)
    vendedor = db.Column(db.Integer)
    sucursal = db.Column(db.Integer)
    num_factura = db.Column(db.BigInteger, nullable=True)  # puede tener valores grandes o estar vacío
    total_facturado = db.Column(db.Float)
    fecha_real = db.Column(db.Date)
    anticipo = db.Column(db.Float)
    financiacion = db.Column(db.Float)
    num_cuotas = db.Column(db.Integer)
    vto_primer_cuota = db.Column(db.Date)

    artic1 = db.Column(db.String, nullable=True)
    cant1 = db.Column(db.Float, nullable=True)
    artic2 = db.Column(db.String, nullable=True)
    cant2 = db.Column(db.Float, nullable=True)
    artic3 = db.Column(db.String, nullable=True)
    cant3 = db.Column(db.Float, nullable=True)
    artic4 = db.Column(db.String, nullable=True)
    cant4 = db.Column(db.Float, nullable=True)
    artic5 = db.Column(db.String, nullable=True)
    cant5 = db.Column(db.Float, nullable=True)
    artic6 = db.Column(db.String, nullable=True)
    cant6 = db.Column(db.Float, nullable=True)
    artic7 = db.Column(db.String, nullable=True)
    cant7 = db.Column(db.Float, nullable=True)

    garante = db.Column(db.String, nullable=True)
    dom_garante = db.Column(db.String, nullable=True)
    estado = db.Column(db.String, default="activo")
