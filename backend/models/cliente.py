from models import db
class Cliente(db.Model):
    __tablename__ = 'clientes'

    documento = db.Column(db.String(20), primary_key=True)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    domicilio = db.Column(db.String(150))
    estado = db.Column(db.String(20), default='pendiente')

    creditos = db.relationship('Credito', backref='cliente', lazy=True)
