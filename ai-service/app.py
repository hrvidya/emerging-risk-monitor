from flask import Flask, jsonify, g
from datetime import datetime
import logging
import time

from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp
from routes.stream_report import stream_report_bp
from routes.analyse_document import analyse_document_bp
from routes.batch_process import batch_process_bp

from services.runtime_metrics import (
    record_latency_ms,
    get_runtime_stats
)

from services.model_loader import get_model

app = Flask(__name__)

# -------------------------
# Preload embedding model
# -------------------------
embedding_model = get_model()

# -------------------------
# Logging setup
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------
# App start time
# -------------------------
start_time = datetime.utcnow()


def get_uptime():
    return str(
        int((datetime.utcnow() - start_time).total_seconds())
    ) + " seconds"


# -------------------------
# Request timing
# -------------------------
@app.before_request
def start_timer():
    g.start_time = time.time()


# -------------------------
# Register blueprints
# -------------------------
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(generate_report_bp)
app.register_blueprint(stream_report_bp)
app.register_blueprint(analyse_document_bp)
app.register_blueprint(batch_process_bp)


# -------------------------
# Health API
# -------------------------
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "running",
        "model": "llama3",
        "uptime": get_uptime()
    })


# -------------------------
# Runtime metrics API
# -------------------------
@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(get_runtime_stats())


# -------------------------
# Home route
# -------------------------
@app.route('/')
def home():
    return "AI Service is running"


# -------------------------
# Security headers + metrics
# -------------------------
@app.after_request
def add_headers(response):
    latency = (time.time() - g.start_time) * 1000
    record_latency_ms(latency)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"

    return response


# -------------------------
# Global error handler
# -------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unhandled error: {str(e)}")

    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


# -------------------------
# Run server
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)