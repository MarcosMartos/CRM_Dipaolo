from flask import Blueprint, request, jsonify
from auth import admin_required
import os

files_bp = Blueprint("files", __name__)
UPLOAD_FOLDER = "uploads"

@files_bp.route("/upload", methods=["POST"])
@admin_required
def upload_files():
    # ✅ Solo entra aquí si es POST (no necesitamos preocuparnos de OPTIONS ahora)
    
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

    return jsonify({"mensaje": "Archivos cargados y almacenados correctamente"}), 200
