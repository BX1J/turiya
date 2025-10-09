from flask import Flask, render_template, request, jsonify
from downloader import start_download, get_progress

app = Flask(__name__)

# ... your existing index route stays ...
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
x``

@app.route("/api/start", methods=["POST"])
def api_start():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    mode = (data.get("mode") or "smart").strip().lower()
    quality = (data.get("quality") or "best").strip().lower()
    custom_path = data.get("path") or None

    if not url:
        return jsonify({"ok": False, "message": "URL is required."}), 400

    audio_only = (mode == "audio") or (quality == "audio")
    task_id = start_download(url, mode=mode, quality=quality, path=custom_path, audio_only=audio_only)
    return jsonify({"ok": True, "task_id": task_id})

@app.route("/api/progress", methods=["GET"])
def api_progress():
    task_id = request.args.get("task_id", "").strip()
    if not task_id:
        return jsonify({"ok": False, "message": "task_id is required"}), 400
    prog = get_progress(task_id)
    if not prog:
        return jsonify({"ok": False, "message": "not found"}), 404
    return jsonify({"ok": True, "progress": prog})