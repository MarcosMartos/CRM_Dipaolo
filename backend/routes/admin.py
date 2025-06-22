# backend/routes/admin.py
from flask import Blueprint, jsonify
from threading import Thread
from cargar_todo import cargar_todo

bp = Blueprint('admin', __name__)

@bp.route('/cargar_datos', methods=['POST'])
def cargar_datos():
    Thread(target=cargar_todo).start()
    return jsonify({"mensaje": "Carga iniciada en segundo plano"}), 202
