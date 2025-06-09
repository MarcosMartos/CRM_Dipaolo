from models import db
from app import app  # Asegurate de importar tu instancia de Flask

with app.app_context():
    db.drop_all()   # Borra todas las tablas
    db.create_all() # Crea las tablas según los modelos
