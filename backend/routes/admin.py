# backend/routes/admin.py
from flask import Blueprint, jsonify
from flask_cors import cross_origin
from auth import admin_required
from utils.load_csv_to_db import cargar_todos_los_datos
import logging

bp = Blueprint('admin', __name__)

@bp.route('/cargar_datos', methods=['POST'])
@cross_origin()
@admin_required
def cargar_datos():
    try:
        mensaje, status = cargar_todos_los_datos()
        logging.info(f"Resultado de carga: {mensaje}")
        return jsonify({"mensaje": mensaje}), status
    except Exception as e:
        logging.error(f"Error inesperado al cargar datos: {e}")
        return jsonify({"error": str(e)}), 500
