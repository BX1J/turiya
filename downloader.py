import os
import threading
import uuid
from typing import Dict, Any, Optional

from yt_dlp import YoutubeDL

# In-memory progress storage: task_id -> progress dict
progress_store: Dict[str, Dict[str, Any]] = {}

def _build_output_dir(path: Optional[str]) -> str:
    downloads_path = path if path else os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(downloads_path, exist_ok=True)
    return downloads_path

def _make_format(mode: str, quality: str) -> str:
    mode = (mode or "smart").lower()
    quality = (quality or "best").lower()
    if mode == "audio" or quality == "audio":
        return "bestaudio/best"
    # Keep it simple for v1; you can refine mappings later
    if quality in {"1080p", "720p", "480p"}:
        # Prefer bestvideo up to target height + bestaudio, else best
        mapping = {
            "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        }
        return mapping[quality]
    return "bestvideo+bestaudio/best"

def _progress_hook(task_id: str):
    def hook(d: Dict[str, Any]):
        state = progress_store.get(task_id, {})
        if d.get("status") == "downloading":
            percent = 0.0
            if d.get("_percent_str"):
                try:
                    percent = float(d["_percent_str"].strip().strip("%"))
                except Exception:
                    percent = state.get("percent", 0.0)
            eta = d.get("eta")
            speed = d.get("speed")
            state.update({
                "status": "downloading",
                "percent": percent,
                "eta": eta,
                "speed": speed,
                "filename": d.get("filename") or state.get("filename"),
            })
            progress_store[task_id] = state
        elif d.get("status") == "finished":
            state.update({"status": "postprocessing", "percent": 100.0})
            progress_store[task_id] = state
    return hook

def _run_download(task_id: str, url: str, mode: str, quality: str, path: Optional[str], audio_only_flag: bool):
    progress_store[task_id] = {"status": "starting", "percent": 0.0}
    output_dir = _build_output_dir(path)
    outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")

    # Decide format
    if audio_only_flag:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "noplaylist": True,
            "progress_hooks": [_progress_hook(task_id)],
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
            ],
        }
    else:
        ydl_opts = {
            "format": _make_format(mode, quality),
            "outtmpl": outtmpl,
            "noplaylist": True,
            "progress_hooks": [_progress_hook(task_id)],
            "merge_output_format": "mp4",
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
        progress_store[task_id].update({
            "status": "complete",
            "done": True,
            "filepath": filepath,
            "percent": 100.0
        })
    except Exception as e:
        progress_store[task_id].update({
            "status": "error",
            "done": True,
            "error": str(e)
        })

def start_download(url: str, mode: str = "smart", quality: str = "best", path: Optional[str] = None, audio_only: bool = False) -> str:
    task_id = uuid.uuid4().hex
    t = threading.Thread(
        target=_run_download,
        args=(task_id, url, mode, quality, path, audio_only),
        daemon=True
    )
    t.start()
    return task_id

def get_progress(task_id: str) -> Dict[str, Any]:
    return progress_store.get(task_id, {})