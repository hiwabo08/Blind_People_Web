# File: backend/run.py
# Run with: python run.py
# Requirements: flask
# pip install flask

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import time
from model import simulate_video_analysis, process_contact_form

# Create Flask app - note template_folder and static_folder point to project-level folders
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
)

# Basic home route - serves single-page app
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint for simulated video analysis (video upload or live simulation)
@app.route("/api/video-analysis", methods=["POST"])
def video_analysis():
    """
    Accepts:
      - multipart/form-data with 'video' file (optional)
      - or JSON with {"live": true, "tick": n} for live simulation
    Returns:
      JSON containing:
        - detected_objects: [{name, confidence, warning_flag}]
        - audioDescription: string (TTS transcript)
        - meta: processing_time_ms, source ("upload"|"live")
    """
    start = time.time()
    source = "unknown"
    uploaded_filename = None
    # If content-type is multipart/form-data, handle file
    if request.files and 'video' in request.files:
        video = request.files['video']
        filename = secure_filename(video.filename or "upload.mp4")
        # NOTE: We will not store file long-term; if you want to save, uncomment next lines
        # tmp_path = os.path.join("/tmp", filename)
        # video.save(tmp_path)
        uploaded_filename = filename
        source = "upload"
        # pass name to model to influence mock result
        analysis = simulate_video_analysis(source=source, filename=uploaded_filename)
    else:
        # try JSON body for live simulation
        data = request.get_json(silent=True) or {}
        if data.get("live"):
            source = "live"
            tick = int(data.get("tick", 0))
            analysis = simulate_video_analysis(source=source, tick=tick)
        else:
            # fallback: empty analysis
            source = "none"
            analysis = simulate_video_analysis(source=source)
    elapsed_ms = int((time.time() - start) * 1000)
    resp = {
        "detected_objects": analysis["detected_objects"],
        "audioDescription": analysis["audioDescription"],
        "meta": {
            "processing_time_ms": elapsed_ms,
            "source": source,
            "filename": uploaded_filename,
            "timestamp": analysis.get("timestamp")
        }
    }
    return jsonify(resp), 200

# Contact endpoint - placeholder for storing contact requests / integrating DB
@app.route("/contact", methods=["POST"])
def contact():
    """
    Expects JSON:
      { name, email, message }
    Returns success/failure JSON.
    """
    data = request.get_json(silent=True) or {}
    name = data.get("name", "")
    email = data.get("email", "")
    message = data.get("message", "")
    # Call model helper (mock) to process / validate contact
    ok, info = process_contact_form(name=name, email=email, message=message)
    if ok:
        return jsonify({"status": "success", "info": info}), 200
    else:
        return jsonify({"status": "error", "info": info}), 400

if __name__ == "__main__":
    # Run dev server on port 5000. In production, use gunicorn/uwsgi.
    app.run(host="0.0.0.0", port=5000, debug=True)
