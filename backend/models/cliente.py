from models import db

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    apellido = db.Column(db.String)
    documento = db.Column(db.String, unique=True)
    telefono = db.Column(db.String)
    domicilio = db.Column(db.String)
    historial_atraso = db.Column(db.Integer, default=0)  # cantidad de cuotas atrasadas totales
