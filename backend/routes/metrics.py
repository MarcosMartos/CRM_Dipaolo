from flask import Blueprint, jsonify
from utils.metrics import get_client_metrics, get_credit_metrics

metrics_bp = Blueprint('metrics', __name__, url_prefix='/api/metrics')

@metrics_bp.route('/creditos', methods=['GET'])
def creditos():
    try:
        data = get_credit_metrics()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@metrics_bp.route('/clientes', methods=['GET'])
def clientes():
    try:
        data = get_client_metrics()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
