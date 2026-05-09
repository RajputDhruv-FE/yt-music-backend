# YouTube Playlist Music Player - Backend (Phase 1)

This backend provides two endpoints:

- `GET /playlist?url=` - extracts playlist metadata with `yt_dlp` (no downloads)
- `GET /stream/{video_id}` - returns a fresh direct audio stream URL for a given video id

Development and running (using a virtual environment)

Windows (PowerShell):

```powershell
# create venv in backend/.venv
python -m venv .venv
# activate
.\.venv\Scripts\Activate.ps1
# install
pip install -r requirements.txt
# run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

macOS / Linux (bash/zsh):

```bash
# create venv in backend/.venv
python3 -m venv .venv
# activate
source .venv/bin/activate
# install
pip install -r requirements.txt
# run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Notes:
- Stream URLs are generated dynamically using `yt_dlp` and are not stored.
- This is Phase 1: direct stream URLs only (no proxy streaming).

Scripts:
- `venv_setup.ps1` — PowerShell helper to create and activate a venv and install requirements.
- `setup_venv.sh` — POSIX shell helper for macOS/Linux.

Environment variables

Copy `.env.example` to `.env` and edit as needed. By default CORS_ORIGINS is set to `http://localhost:5173` for the frontend dev server.

Troubleshooting

- If `Activate.ps1` is blocked on Windows, run PowerShell as Administrator and allow script execution or use `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.
- If `yt_dlp` extraction fails for some videos, ensure you have network access and the video is available.

