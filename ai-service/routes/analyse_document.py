from flask import Blueprint, request, jsonify

analyse_document_bp = Blueprint("analyse_document", __name__)


@analyse_document_bp.route("/analyse-document", methods=["POST"])
def analyse_document():

    data = request.get_json()

    # Input validation
    if not data or "text" not in data:
        return jsonify({
            "status": "error",
            "message": "Invalid input"
        }), 400

    text = data["text"]

    if not isinstance(text, str) or not text.strip():
        return jsonify({
            "status": "error",
            "message": "Text must be non-empty"
        }), 400

    # Simulated AI analysis
    findings = [
        {
            "type": "Risk",
            "severity": "HIGH",
            "description": f"Potential issue detected related to: {text}"
        },
        {
            "type": "Observation",
            "severity": "MEDIUM",
            "description": "Requires additional monitoring"
        }
    ]

    return jsonify({
        "status": "success",
        "data": {
            "summary": f"Document analysed successfully for: {text}",
            "findings": findings
        }
    }), 200