#!/bin/sh
# Linux/macOS launcher: ./start.sh
# Starts the app in the background and opens its window. You can close the terminal afterwards:
# the app quits on its own a few minutes after you close its window. Messages go to workspace/app.log.
cd "$(dirname "$0")" || exit 1
PY=$(command -v python3 || command -v python)
if [ -z "$PY" ]; then
    echo "Python 3 isn't installed. On Ubuntu/Debian: sudo apt install python3"
    exit 1
fi
mkdir -p workspace
nohup "$PY" app.py >> workspace/app.log 2>&1 &
echo "learn/programming is starting. Its window opens in a moment."
