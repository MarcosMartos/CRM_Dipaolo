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
    if 'cremae' not in request.files or 'crepag' not in request.files:
        return jsonify({"error": "Faltan archivos cremae o crepag"}), 400

    cremae = request.files['cremae']
    crepag = request.files['crepag']

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Guardar archivos DBF
    cremae_path = os.path.join(UPLOAD_FOLDER, "cremae.dbf")
    crepag_path = os.path.join(UPLOAD_FOLDER, "crepag.dbf")
    cremae.save(cremae_path)
    crepag.save(crepag_path)

    try:
        # Procesar: convertir DBF a CSV
        convertir_cremae()
        convertir_crepag()
        generar_clientes()

        # Cargar CSV a la base de datos
        cargar_creditos("data/creditos.csv")
        cargar_pagos("data/pagos.csv")
        cargar_clientes("data/clientes.csv")

        # Actualizar estado de los clientes
        actualizar_estado_clientes()

        return jsonify({"mensaje": "Archivos procesados y cargados correctamente"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Ocurrió un error al procesar los archivos"}), 500
