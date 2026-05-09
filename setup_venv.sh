#!/usr/bin/env bash
set -e
PY=${1:-python3}
ROOT_DIR="$(dirname "$0")"
VENV_DIR="$ROOT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
  "$PY" -m venv "$VENV_DIR"
fi
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$ROOT_DIR/requirements.txt"
echo "Setup complete. Run: uvicorn app.main:app --reload"
