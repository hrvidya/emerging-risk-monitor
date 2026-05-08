from flask import Blueprint, request, jsonify
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter

generate_report_bp = Blueprint("generate_report", __name__)

# ⚠️ Separate limiter instance for route-level control
limiter = Limiter(key_func=get_remote_address)


@generate_report_bp.route("/generate-report", methods=["POST"])
@limiter.limit("10 per minute")  #  STRICT LIMIT (Day 4)
def generate_report():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "status": "error",
            "message": "Invalid input"
        }), 400

    text = data["text"]

    # ✅ Day 9: Simulated AI response + fallback
    try:
        ai_response = {
            "title": "Risk Analysis Report",
            "executive_summary": f"This report summarizes risks related to: {text}",
            "overview": f"The scenario involves potential risks in: {text}",
            "top_items": [
                f"Risk identified in: {text}",
                "Possible system impact",
                "Requires monitoring and mitigation"
            ],
            "recommendations": [
                "Implement monitoring mechanisms",
                "Strengthen security controls",
                "Conduct regular audits"
            ]
        }
    except Exception:
        ai_response = {
            "title": "Fallback Report",
            "executive_summary": "Error generating report"
        }

    return jsonify({
        "status": "success",
        "data": {
            "report": ai_response
        }
    }), 200