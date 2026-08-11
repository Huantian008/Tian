"""
全国空气质量可视化分析大屏 - Flask后端API
"""

from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from api.air_quality import generate_dashboard


API_DIR = Path(__file__).resolve().parent
DIST_DIR = API_DIR.parent / "dist"
DATA_FILE = API_DIR / "data" / "air_quality_dashboard.json"

app = Flask(__name__, static_folder=str(DIST_DIR), static_url_path="")
CORS(app)


def get_dashboard_data() -> dict[str, object]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    dashboard = generate_dashboard()
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(dashboard, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return dashboard


@app.route("/")
def index():
    return send_from_directory(DIST_DIR, "index.html")


@app.route("/api/dashboard")
def dashboard():
    return jsonify(get_dashboard_data())


@app.route("/api/refresh")
def refresh():
    return jsonify(get_dashboard_data())


@app.route("/api/map")
def map_data():
    return jsonify(get_dashboard_data()["mapPoints"])


@app.route("/api/city-rank")
def city_rank():
    return jsonify(get_dashboard_data()["cityRank"])


@app.route("/api/trend")
def trend():
    return jsonify(get_dashboard_data()["trend"])


@app.route("/api/pollutants")
def pollutants():
    return jsonify(get_dashboard_data()["pollutantMix"])


@app.route("/api/heatmap")
def heatmap():
    return jsonify(get_dashboard_data()["cityHeatmap"])


@app.route("/api/levels")
def levels():
    return jsonify(get_dashboard_data()["levelDistribution"])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
