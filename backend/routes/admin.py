from flask import Blueprint, jsonify, g
from auth import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
@admin_required
def admin_zone():
    return jsonify({"mensaje": f"Hola admin {g.user['email']}!"})
