from models import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default='usuario')

    def set_password(self, password_plain):
        self.password = generate_password_hash(password_plain)

    def check_password(self, password_plain):
        return check_password_hash(self.password, password_plain)
