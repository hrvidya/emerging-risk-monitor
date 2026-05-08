from flask import Blueprint, request, jsonify
import time
import logging
import os

from services.cache_service import (
    get_cached_response,
    set_cached_response
)

describe_bp = Blueprint("describe", __name__)

request_log = {}
RATE_LIMIT = 5
TIME_WINDOW = 60


def is_rate_limited(ip):
    current_time = time.time()

    if ip not in request_log:
        request_log[ip] = []

    request_log[ip] = [
        t for t in request_log[ip]
        if current_time - t < TIME_WINDOW
    ]

    if len(request_log[ip]) >= RATE_LIMIT:
        return True

    request_log[ip].append(current_time)
    return False


def load_prompt():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        prompt_path = os.path.abspath(
            os.path.join(base_dir, "..", "prompts", "describe.txt")
        )

        with open(prompt_path, "r") as f:
            return f.read()

    except Exception as e:
        logging.error(f"Prompt load error: {str(e)}")
        return None


@describe_bp.route("/describe", methods=["POST"])
def describe():

    client_ip = request.remote_addr

    # Rate limit check
    if is_rate_limited(client_ip):
        return jsonify({
            "status": "error",
            "message": "Too many requests. Try again later."
        }), 429

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

    if len(text) > 500:
        return jsonify({
            "status": "error",
            "message": "Input too long"
        }), 400

    # Cache check
    cached = get_cached_response(text)

    if cached:
        return jsonify({
            "status": "success",
            "cached": True,
            "data": cached
        }), 200

    # Prompt injection protection
    blocked_words = [
        "ignore previous",
        "system prompt",
        "override",
        "bypass"
    ]

    for word in blocked_words:
        if word in text.lower():
            logging.warning(f"Blocked malicious input: {text}")

            return jsonify({
                "status": "error",
                "message": "Unsafe input detected"
            }), 400

    # Load prompt
    prompt_template = load_prompt()

    if not prompt_template:
        return jsonify({
            "status": "error",
            "message": "Prompt file not found"
        }), 500

    final_prompt = prompt_template.replace("{input}", text)

    # Simulated AI response
    try:
        ai_output = f"Processed safely: {text}"

    except Exception:
        ai_output = "Error generating description"

    response_data = {
        "input": text,
        "generated_prompt": final_prompt,
        "description": ai_output
    }

    # Store in cache
    set_cached_response(text, response_data)

    return jsonify({
        "status": "success",
        "cached": False,
        "data": response_data
    }), 200