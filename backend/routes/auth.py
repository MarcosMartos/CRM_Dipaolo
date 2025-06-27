from flask import Blueprint, request, jsonify
from models import db, Usuario
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from functools import wraps
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

# === FUNCIONES AUXILIARES ===

def generar_token(usuario):
    payload = {
        "user_id": usuario.id,
        "email": usuario.email,
        "rol": usuario.rol,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        token = auth_header.replace("Bearer ", "")
        try:
            decoded = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            if decoded.get("rol") != "admin":
                return jsonify({"error": "Permisos insuficientes"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)
    return decorated_function

# === RUTAS ===

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Usuario ya existe"}), 400

    nuevo_usuario = Usuario(
        nombre=data["nombre"],
        email=data["email"],
        rol=data.get("rol", "usuario"),
        password_hash=generate_password_hash(data["password"])
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado correctamente"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(email=data["email"]).first()

    if not usuario or not check_password_hash(usuario.password_hash, data["password"]):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    token = generar_token(usuario)
    return jsonify({"token": token})
