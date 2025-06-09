# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos (importaciones abajo para evitar bucles)
from .usuario import Usuario
from .credito import Credito
from .pago import Pago
from .cliente import Cliente
