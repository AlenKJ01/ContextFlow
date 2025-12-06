# backend/app.py

import os
from flask import Flask, render_template
from backend.routes.memory_routes import memory_bp
from backend.routes.personality_routes import personality_bp
from backend.routes.healthcheck import health_bp
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(ROOT, "templates"),
    static_folder=None
)

# Register blueprints
app.register_blueprint(health_bp)                 # /health
app.register_blueprint(memory_bp, url_prefix="/memory")
app.register_blueprint(personality_bp, url_prefix="/personality")

# Home UI
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Debug: list available models
@app.route("/models", methods=["GET"])
def list_models():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return {"error": "GEMINI_API_KEY not set"}, 500

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    try:
        resp = requests.get(url, timeout=20)
        return resp.text
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
