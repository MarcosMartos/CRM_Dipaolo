from flask import Blueprint, request, jsonify
from auth import admin_required
import os

from utils.convert_dbf_to_csv import convertir_creditos, convertir_pagos, generar_clientes

files_bp = Blueprint("files", __name__)
UPLOAD_FOLDER = "uploads"

def ejecutar_procesamiento():
    convertir_creditos()
    convertir_pagos()
    generar_clientes()

@files_bp.route("/upload", methods=["POST"])
@admin_required
def upload_files():
    try:
        if 'cremae' not in request.files or 'crepag' not in request.files:
            return jsonify({"error": "Faltan archivos cremae o crepag"}), 400

        cremae = request.files['cremae']
        crepag = request.files['crepag']

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        cremae_path = os.path.join(UPLOAD_FOLDER, "cremae.dbf")
        crepag_path = os.path.join(UPLOAD_FOLDER, "crepag.dbf")
        cremae.save(cremae_path)
        crepag.save(crepag_path)

        ejecutar_procesamiento()

        return jsonify({"mensaje": "Archivos cargados y CSVs generados correctamente. Ejecutá /admin/cargar_datos para cargar en BD."}), 200

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print("❌ ERROR INTERNO EN /files/upload:\n", error_trace)
        return jsonify({"error": str(e), "detalle": error_trace}), 500
