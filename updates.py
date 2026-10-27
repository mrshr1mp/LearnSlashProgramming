"""Keeps everyone's copy of the app up to date with the GitHub repo.

Updates only ever touch the app's own files. Your code and progress live in workspace/,
which git ignores, so an update can never change or delete them.
"""
import os
import shutil
import subprocess
import threading
import time

import learn

# never pop up a GitHub sign-in from the background: if git can't fetch quietly, just skip the update
ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"}
status = {"available": False, "changes": [], "error": None}


def _git(*args, timeout=20):
    r = subprocess.run(["git", *args], cwd=learn.ROOT, capture_output=True, encoding="utf-8", errors="replace",
                       timeout=timeout, env=ENV)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def enabled():
    """Only copies made with `git clone` can update themselves."""
    return (learn.ROOT / ".git").exists() and shutil.which("git") is not None


def version():
    # the installed app updates itself (Tauri's updater) and tells us its version number
    return os.environ.get("LEARN_VERSION") or (_git("rev-parse", "--short", "HEAD")[1] if enabled() else "") or "local"


def check():
    """Ask GitHub for anything new. Returns what changed (newest first), or [] if up to date or offline."""
    if not enabled():
        return []
    try:
        code, _, err = _git("fetch", "--quiet")
    except subprocess.TimeoutExpired:
        return []
    if code:
        status["error"] = err
        return []
    code, out, _ = _git("log", "--format=%s", "HEAD..@{upstream}")
    changes = out.splitlines() if code == 0 and out else []
    status.update(available=bool(changes), changes=changes[:8], error=None)
    return changes


def apply():
    """Download the update. Returns (ok, message)."""
    try:
        code, out, err = _git("pull", "--ff-only", "--quiet", timeout=90)
    except subprocess.TimeoutExpired:
        return False, "GitHub took too long to answer"
    if code:
        return False, err or out
    status.update(available=False, changes=[])
    return True, ""


def check_in_background(every=600):
    def loop():
        while True:
            check()
            time.sleep(every)
    threading.Thread(target=loop, daemon=True).start()
