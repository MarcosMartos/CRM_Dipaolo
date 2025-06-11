from flask import Blueprint, jsonify
from auth import admin_required
from utils import metrics

metrics_bp = Blueprint("metrics", __name__)

@metrics_bp.route("/", methods=["GET"])
@admin_required
def obtener_metrics():
    data = {
        "generales": {
            "cantidad_creditos_totales": metrics.cantidad_creditos_totales(),
            "importe_total_creditos": metrics.importe_total_creditos(),
        },
        "creditos_activos": {
            "cantidad": metrics.cantidad_creditos_activos(),
            "importe_total": metrics.importe_total_activos(),
            "pagado_total": metrics.pagado_total_activos(),
            "deuda_total": metrics.deuda_total_activos(),
            "porcentaje_pagado": metrics.porcentaje_pagado(),
            "porcentaje_deuda": metrics.porcentaje_deuda()
        },
        "clientes": {
            "cantidad_excelentes": metrics.contar_clientes_por_estado("excelente"),
            "porcentaje_excelentes": metrics.porcentaje_clientes("excelente"),
            "cantidad_buenos": metrics.contar_clientes_por_estado("bueno"),
            "porcentaje_buenos": metrics.porcentaje_clientes("bueno"),
            "cantidad_remolones": metrics.contar_clientes_por_estado("remolon"),
            "porcentaje_remolones": metrics.porcentaje_clientes("remolon"),
            "cantidad_malos": metrics.contar_clientes_por_estado("malo"),
            "porcentaje_malos": metrics.porcentaje_clientes("malo"),
        }
    }
    return jsonify(data)
