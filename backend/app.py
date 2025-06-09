from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from models import db, Usuario, Credito, Pago, Cliente

# Cargar variables de entorno
load_dotenv()

# Crear la app
app = Flask(__name__)

# Configuración de CORS global (antes de cualquier blueprint)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

# Configurar base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar base de datos y migraciones
db.init_app(app)
migrate = Migrate(app, db)

# Importar blueprints
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.files import files_bp
from routes.metrics import metrics_bp

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(files_bp, url_prefix="/files")
app.register_blueprint(metrics_bp, url_prefix="/metrics")

# Ruta base de prueba
@app.route("/")
def index():
    return "Servidor Flask funcionando correctamente"

# Crear tablas al iniciar la app
with app.app_context():
    db.create_all()

# Ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True)
