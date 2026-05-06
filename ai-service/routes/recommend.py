from flask import Blueprint, request, jsonify
import os

recommend_bp = Blueprint("recommend", __name__)

def load_prompt():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.abspath(
            os.path.join(base_dir, "..", "prompts", "recommend.txt")
        )
        with open(prompt_path, "r") as file:
            return file.read()
    except Exception:
        return None


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "status": "error",
            "message": "Invalid input"
        }), 400

    text = data["text"]

    prompt_template = load_prompt()

    if not prompt_template:
        return jsonify({
            "status": "error",
            "message": "Prompt file not found"
        }), 500

    final_prompt = prompt_template.replace("{text}", text)

    # ✅ Day 9: Simulated AI recommendations + fallback
    try:
        ai_recommendations = [
            {
                "action_type": "Monitor",
                "description": f"Monitor risk related to: {text}",
                "priority": "HIGH"
            },
            {
                "action_type": "Mitigate",
                "description": f"Take mitigation steps for: {text}",
                "priority": "MEDIUM"
            }
        ]
    except Exception:
        ai_recommendations = []

    return jsonify({
        "status": "success",
        "data": {
            "prompt_used": final_prompt,
            "recommendations": ai_recommendations
        }
    }), 200