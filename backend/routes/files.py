from flask import Blueprint, request, jsonify
from auth import admin_required
import os

from utils.dbf_to_csv import convertir_cremae, convertir_crepag, generar_clientes
from utils.csv_to_db import cargar_creditos, cargar_pagos, cargar_clientes
from utils.actualizar_clientes import actualizar_estado_clientes

files_bp = Blueprint("files", __name__)
UPLOAD_FOLDER = "uploads"

@files_bp.route("/upload", methods=["POST"])
@admin_required
def upload_files():
    try:
        # Validar archivos
        if 'cremae' not in request.files or 'crepag' not in request.files:
            return jsonify({"error": "Faltan archivos cremae o crepag"}), 400

        cremae = request.files['cremae']
        crepag = request.files['crepag']

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Guardar archivos
        cremae_path = os.path.join(UPLOAD_FOLDER, "cremae.dbf")
        crepag_path = os.path.join(UPLOAD_FOLDER, "crepag.dbf")
        cremae.save(cremae_path)
        crepag.save(crepag_path)

        # === PROCESO DE CONVERSIÓN Y CARGA ===
        convertir_cremae()
        convertir_crepag()
        generar_clientes()

        cargar_creditos("data/creditos.csv")
        cargar_pagos("data/pagos.csv")
        cargar_clientes("data/clientes.csv")

        actualizar_estado_clientes()

        return jsonify({"mensaje": "Archivos procesados y cargados correctamente"}), 200

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print("❌ ERROR INTERNO EN /files/upload:\n", error_trace)
        return jsonify({"error": str(e), "detalle": error_trace}), 500
