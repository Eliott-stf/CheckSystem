from flask import Blueprint, jsonify

from ..services.stats_cache import get_quick_stats
from ..services.system_metrics import get_live_monitoring_data

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

@api_blueprint.route("/quick-stats")
def quick_stats():
  return jsonify(get_quick_stats())
  try:
    return jsonify(get_quick_stats())
  except Exception as exc:
    return jsonify({"error": str(exc)}), 500

@api_blueprint.route("/live-monitoring")
def live_monitoring():
  try:
    return jsonify(get_live_monitoring_data)
  except Exception as exc:
    return jsonify({"error": str(exc)}), 500