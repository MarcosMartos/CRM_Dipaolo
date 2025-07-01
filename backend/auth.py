import jwt
import os
from flask import request, jsonify, g
from functools import wraps
from models import Usuario
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

# Generar token JWT
def generar_token(usuario):
    payload = {
        "user_id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rol": usuario.rol
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Verificar token JWT
def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Decorador login_required (para usuarios normales)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "OPTIONS":
            return f(*args, **kwargs)  # Permitimos pasar el preflight de CORS

        auth_header = request.headers.get('Authorization', '').strip()
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token requerido"}), 401

        token = auth_header.replace("Bearer ", "").strip()
        if not token:
            return jsonify({"error": "Token vacío"}), 401

        payload = verificar_token(token)
        if not payload:
            return jsonify({"error": "Token inválido o expirado"}), 401

        g.user = payload
        return f(*args, **kwargs)
    return decorated_function

# Decorador admin_required (para proteger rutas de admin)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "OPTIONS":
            return f(*args, **kwargs)  # Permitimos pasar el preflight de CORS

        auth_header = request.headers.get('Authorization', '').strip()
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token requerido"}), 401

        token = auth_header.replace("Bearer ", "").strip()
        if not token:
            return jsonify({"error": "Token vacío"}), 401

        payload = verificar_token(token)
        if not payload:
            return jsonify({"error": "Token inválido o expirado"}), 401

        if payload.get("rol") != "admin":
            return jsonify({"error": "Acceso denegado: se requiere rol admin"}), 403

        g.user = payload
        return f(*args, **kwargs)
    return decorated_function
