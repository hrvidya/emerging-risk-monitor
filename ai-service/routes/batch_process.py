from flask import Blueprint, request, jsonify
import time

batch_process_bp = Blueprint("batch_process", __name__)


@batch_process_bp.route("/batch-process", methods=["POST"])
def batch_process():

    data = request.get_json()

    # Validation
    if not data or "items" not in data:
        return jsonify({
            "status": "error",
            "message": "Invalid input"
        }), 400

    items = data["items"]

    if not isinstance(items, list):
        return jsonify({
            "status": "error",
            "message": "Items must be a list"
        }), 400

    if len(items) == 0:
        return jsonify({
            "status": "error",
            "message": "Items list cannot be empty"
        }), 400

    if len(items) > 20:
        return jsonify({
            "status": "error",
            "message": "Maximum 20 items allowed"
        }), 400

    results = []

    for item in items:

        # Simulate processing delay (100ms)
        time.sleep(0.1)

        results.append({
            "input": item,
            "status": "processed",
            "description": f"Processed item: {item}"
        })

    return jsonify({
        "status": "success",
        "data": {
            "count": len(results),
            "results": results
        }
    }), 200