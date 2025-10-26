# File: backend/model.py
# Mock business logic and simulated AI responses.
# This is intentionally simple and deterministic for testing/demo purposes.

import time
from datetime import datetime

def _now_iso():
    return datetime.utcnow().isoformat() + "Z"

def simulate_video_analysis(source="upload", filename=None, tick=0):
    """
    Returns a simulated analysis result.
    - source: "upload" or "live" or "none"
    - filename: optional uploaded filename (affects returned text)
    - tick: integer tick for live simulation (changes results over time)
    """
    # small simulated processing delay to mimic real work (keep short)
    time.sleep(0.6)

    # vary results by tick to show changing live stream analysis
    base_objs = [
        {"name": "person", "confidence": 0.98, "warning_flag": False},
        {"name": "chair", "confidence": 0.88, "warning_flag": False},
        {"name": "staircase", "confidence": 0.79, "warning_flag": True},
    ]

    # mutate based on tick
    if source == "live":
        # cycle through different scenarios depending on tick
        t = tick % 5
        if t == 0:
            objs = base_objs
            audio = "Person ahead. Chair to the right. Stairs ahead, be careful."
        elif t == 1:
            objs = [
                {"name": "door", "confidence": 0.92, "warning_flag": False},
                {"name": "curb", "confidence": 0.75, "warning_flag": True},
            ]
            audio = "Door detected. Curb 3 feet ahead, watch your step."
        elif t == 2:
            objs = [
                {"name": "exit sign", "confidence": 0.86, "warning_flag": False},
                {"name": "person", "confidence": 0.95, "warning_flag": False},
            ]
            audio = "Sign says: Exit. Two people nearby."
        elif t == 3:
            objs = [
                {"name": "vehicle", "confidence": 0.90, "warning_flag": True},
            ]
            audio = "Vehicle approaching from the left. Move back from the road."
        else:
            objs = base_objs + [{"name": "puddle", "confidence": 0.70, "warning_flag": True}]
            audio = "Puddle detected. Slippery surface ahead."
    elif source == "upload":
        # If user uploaded a file, refer to filename to make it feel personalized
        label = (filename or "uploaded video").split(".")[0]
        objs = [
            {"name": "text sign", "confidence": 0.94, "warning_flag": False},
            {"name": "person", "confidence": 0.89, "warning_flag": False},
        ]
        audio = f"Analysis of {label}: Sign reads 'Welcome'. Person detected nearby."
    else:
        objs = []
        audio = "No video source provided. Use the upload or live stream controls."

    # add minor confidence jitter for demo
    for o in objs:
        o["confidence"] = round(float(o.get("confidence", 0.8)), 2)

    return {
        "detected_objects": objs,
        "audioDescription": audio,
        "timestamp": _now_iso()
    }

def process_contact_form(name, email, message):
    """
    Mock contact processing — validate inputs and pretend to store them.
    Returns (ok: bool, info: str)
    """
    if not name or not email or not message:
        return False, "Missing required fields."
    # Very simple email validation
    if "@" not in email or "." not in email:
        return False, "Invalid email address."
    # simulate storing / sending
    time.sleep(0.2)
    return True, f"Contact saved for {name}. We'll reach out to {email}."
