from flask import Blueprint, request, jsonify
from models import db, Usuario
from auth import generar_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Usuario ya existe"}), 400

    nuevo_usuario = Usuario(
        nombre=data["nombre"],
        email=data["email"],
        rol=data.get("rol", "usuario")
    )
    nuevo_usuario.set_password(data["password"])
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado correctamente"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    usuario = Usuario.query.filter_by(email=data["email"]).first()
  

    if not usuario or not usuario.check_password(data["password"]):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    token = generar_token(usuario)
    return jsonify({"token": token})
