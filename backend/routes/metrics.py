from flask import Blueprint, jsonify
from auth import admin_required
from utils import metrics

metrics_bp = Blueprint("metrics", __name__)

@metrics_bp.route("/", methods=["GET"])
@admin_required
def obtener_metrics():
    data = {
        "cantidad_creditos": metrics.cantidad_creditos(),
        "importe_creditos": metrics.importe_creditos(),
        "pagado_creditos": metrics.pagado_creditos(),
        "deuda_creditos": metrics.deuda_creditos(),
        "creditos_atrasados": metrics.creditos_atrasados(),
        "importe_atrasado": metrics.importe_atrasado(),
        "tasa_recuperacion": metrics.tasa_recuperacion(),
        "clientes_pagadores": metrics.clientes_pagadores(),
        "clientes_remolones": metrics.clientes_remolones(),
        "clientes_malos": metrics.clientes_malos(),
        "tasa_reincidencia": metrics.tasa_reincidencia()
    }
    return jsonify(data)
