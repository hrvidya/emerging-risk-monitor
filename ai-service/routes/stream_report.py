from flask import Blueprint, Response
import time
import json

stream_report_bp = Blueprint("stream_report", __name__)


@stream_report_bp.route("/stream-report", methods=["GET"])
def stream_report():

    def generate():

        messages = [
            {"step": "Analyzing risk data..."},
            {"step": "Generating executive summary..."},
            {"step": "Preparing recommendations..."},
            {"step": "Finalizing report..."},
            {"status": "success"}
        ]

        for message in messages:
            yield f"data: {json.dumps(message)}\n\n"
            time.sleep(2)

    return Response(generate(), mimetype="text/event-stream")