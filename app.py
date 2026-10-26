"""The app. Run `python app.py` and it opens in its own window. Close this console to quit."""
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import cloud
import learn
import updates

PORT = int(os.environ.get("LEARN_PORT", 8765))  # override only if 8765 is taken (or for testing)
HOSTS = {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}
VERSION = updates.version()
OPEN = {"/api/me", "/api/signin", "/api/signup", "/api/quit"}  # everything else needs you signed in
UI = learn.ROOT / "ui.html"
RESULT = re.compile(r"^  (PASS|FAIL|CRASH|TODO)\s+(\S+?)(?::\s?(.*))?$")
FRAME = re.compile(r'File "(.+?)", line (\d+)')
ERROR_LINE = re.compile(r"^([A-Za-z_][\w.]*)(?::\s?(.*))?$")


def same_file(a, b):
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def crash_info(text, solution):
    """Pull the error type and the deepest line of the learner's own file out of a traceback."""
    lines = text.splitlines()
    last = next((l.strip() for l in reversed(lines) if l.strip()), "")
    m = ERROR_LINE.match(last)
    info = {"type": m[1].split(".")[-1], "message": m[2] or ""} if m else {"type": "", "message": last}
    info.update(line=None, code="")
    for i, l in enumerate(lines):
        f = FRAME.search(l)
        if f and same_file(f[1], solution):
            info["line"], info["code"] = int(f[2]), lines[i + 1].strip() if i + 1 < len(lines) else ""
    return info


def parse_results(output, solution):
    """Split the harness's text output into one item per test."""
    results, preamble = [], []
    for line in output.splitlines():
        m = RESULT.match(line)
        if m:
            results.append({"status": m[1], "name": m[2], "message": m[3] or "", "detail": []})
        else:
            (results[-1]["detail"] if results else preamble).append(line)
    if not results and output.strip():  # crashed before any test ran, or timed out
        results.append({"status": "CRASH", "name": "your_file", "message": "", "detail": preamble})
    for r in results:
        r["detail"] = "\n".join(r["detail"]).strip("\n")
        if r["status"] == "CRASH":
            r["error"] = crash_info(r["detail"], solution)
    return results


def mission_info(track, m):
    return {"n": m["n"], "id": m["id"], "title": m["title"], "kind": m["kind"], "xp": m["xp"], "status": m["status"],
            "chapter": m["chapter"], "chapter_n": m["chapter_n"], "file": f"workspace/{track}/{m['file']}"}


def state(track):
    s = learn.summary(track)
    cfg = learn.track_cfg(track)
    ms = [dict(mission_info(track, m), brief=(m["dir"] / "mission.md").read_text(encoding="utf-8")) for m in s["missions"]]
    return {**s, "missions": ms, "track": track, "icon": cfg.get("icon", ""), "logo": cfg.get("logo", ""),
            "errors": cfg.get("errors", {})}


def course_info(track, s):
    cfg = learn.track_cfg(track)
    return {"track": track, "name": s["name"], "icon": cfg.get("icon", ""), "logo": cfg.get("logo", ""),
            "description": cfg.get("description", ""), "xp": s["xp"], "rank": s["rank"], "rank_xp": s["rank_xp"],
            "next": s["next"], "missions": [mission_info(track, m) for m in s["missions"]]}


def overview():
    """Every course's progress, plus a dated log of completed missions."""
    progress = learn.load_progress()
    courses = [course_info(track, learn.summary(track)) for track in learn.tracks()]
    return {"courses": courses, "history": learn.history(progress), "checks": progress.get("_checks", {})}


def friend_overview(username):
    """Same shape as overview(), built from a friend's synced progress."""
    p = cloud.profile(username)
    finished = {}
    for c in p["completions"]:
        finished.setdefault(c["track"], []).append(c["mission_id"])
    readable = {(r["track"], r["mission_id"]) for r in p["readable"]}
    courses = []
    for track in learn.tracks():
        info = course_info(track, learn.summary(track, finished.get(track, [])))
        for m in info["missions"]:
            m["code"] = (track, m["id"]) in readable
        courses.append(info)
    history = sorted(({"track": c["track"], "id": c["mission_id"], "date": c["completed_on"]} for c in p["completions"]),
                     key=lambda h: h["date"])
    return {"username": username, "avatar": p["avatar"], "courses": courses, "history": history,
            "checks": {a["day"]: a["checks"] for a in p["activity"]}}


def me():
    s = cloud.session()
    if not s:
        return {"signed_in": False, "version": VERSION}
    try:
        avatar = cloud.my_avatar()
    except cloud.CloudError:
        avatar = None  # offline: show the letter instead
    return {"signed_in": True, "username": s["username"], "email": s["email"], "avatar": avatar, "sync": cloud.status,
            "version": VERSION, "update": updates.status}


def my_code(track, mission_id):
    m = next((m for m in learn.missions(track) if m["id"] == mission_id), None)
    f = m and learn.WORK / track / m["file"]
    return {"filename": f.name, "code": f.read_text(encoding="utf-8", errors="replace")} if f and f.exists() else None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, body, status=200, kind="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def allowed(self, path):
        # Only this app may talk to this server. The Host check stops DNS-rebinding tricks; the custom
        # header can't be sent by other websites without a CORS preflight, which we never approve.
        if self.headers.get("Host") not in HOSTS:
            return False
        return not path.startswith("/api/") or self.headers.get("X-Kit") == "1"

    def signed_out(self, path):
        """You need an account to use the app; only the sign-in endpoints work without one."""
        if path.startswith("/api/") and path not in OPEN and not cloud.session():
            self.send({"error": "Sign in first"}, 401)
            return True
        return False

    def do_GET(self):
        url = urlparse(self.path)
        if not self.allowed(url.path):
            return self.send({"error": "forbidden"}, 403)
        if self.signed_out(url.path):
            return
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        try:
            if url.path == "/":
                return self.send(UI.read_bytes(), kind="text/html; charset=utf-8")
            if url.path == "/api/overview":
                return self.send(overview())
            if url.path == "/api/state":
                if q.get("track") not in learn.tracks():
                    return self.send({"error": "unknown track"}, 400)
                return self.send(state(q["track"]))
            if url.path == "/api/me":
                return self.send(me())
            if url.path == "/api/friends":
                return self.send(cloud.friends())
            if url.path.startswith("/api/user") and not cloud.USERNAME.match(q.get("name", "")):
                return self.send({"error": "bad username"}, 400)
            if url.path == "/api/user":
                return self.send(friend_overview(q["name"]))
            if url.path == "/api/user/code":
                if q.get("track") not in learn.tracks():
                    return self.send({"error": "unknown track"}, 400)
                return self.send({"theirs": cloud.code(q["name"], q["track"], q.get("mission", "")),
                                  "mine": my_code(q["track"], q.get("mission", ""))})
        except cloud.CloudError as e:
            return self.send({"error": str(e)}, 400)
        self.send({"error": "not found"}, 404)

    def do_POST(self):
        action = urlparse(self.path).path
        if not self.allowed(action):
            return self.send({"error": "forbidden"}, 403)
        if self.signed_out(action):
            return
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        if action == "/api/quit":  # a newer copy of the app is taking over
            self.send({"result": "bye"})
            return threading.Thread(target=self.server.shutdown).start()
        if action == "/api/update":
            ok, message = updates.apply()
            if not ok:
                return self.send({"error": f"Couldn't update: {message}"}, 400)
            self.send({"result": "restarting"})
            return restart()
        try:
            if action == "/api/avatar":
                avatar = body.get("avatar")
                cloud.set_avatar(avatar if isinstance(avatar, str) else None)
                return self.send(me())
            if action == "/api/signup":
                cloud.sign_up(body.get("email", ""), body.get("password", ""), body.get("username", ""))
                cloud.sync()
                return self.send(me())
            if action == "/api/signin":
                cloud.sign_in(body.get("email", ""), body.get("password", ""))
                cloud.sync()
                return self.send(me())
            if action == "/api/signout":
                cloud.sign_out()
                return self.send(me())
            if action.startswith("/api/friends/"):
                name = body.get("username", "")
                if not cloud.USERNAME.match(name):
                    return self.send({"error": "Usernames are 3-20 letters, numbers or _"}, 400)
                if action == "/api/friends/add":
                    return self.send({"result": cloud.add_friend(name)})
                if action == "/api/friends/accept":
                    cloud.accept_friend(name)
                    return self.send({"result": "accepted"})
                if action == "/api/friends/remove":
                    cloud.remove_friend(name)
                    return self.send({"result": "removed"})
        except cloud.CloudError as e:
            return self.send({"error": str(e)}, 400)
        return self.mission_action(action, body)

    def mission_action(self, action, body):
        track, n = body.get("track", "python"), body.get("mission")
        if track not in learn.tracks():
            return self.send({"error": "unknown track"}, 400)
        ms = learn.missions(track)
        if not isinstance(n, int) or not 1 <= n <= len(ms):
            return self.send({"error": "unknown mission"}, 400)
        m = ms[n - 1]
        target = learn.WORK / track / m["file"]

        if action == "/api/start":
            learn.prepare(track, m)
            opened = learn.open_in_editor(target)
            return self.send({"state": state(track), "opened": opened})
        if action == "/api/open":
            line = body.get("line")
            return self.send({"opened": learn.open_in_editor(target, line if isinstance(line, int) else None)})
        if action == "/api/check":
            if not target.exists():
                return self.send({"error": "start the mission first"}, 400)
            before = learn.summary(track)
            learn.log_check()
            passed, output = learn.run_tests(track, m)
            first_time = passed and learn.award(track, m)
            cloud.sync_in_background()
            return self.send({"passed": passed, "first_time": first_time, "output": output,
                              "results": parse_results(output, target),
                              "before": {"xp": before["xp"], "rank": before["rank"]}, "state": state(track)})
        self.send({"error": "not found"}, 404)


class Server(ThreadingHTTPServer):
    allow_reuse_address = False  # on Windows, True would let two copies share the port


def open_window(url):
    """Open as a standalone app window (Edge/Chrome --app mode), falling back to a normal tab."""
    candidates = [shutil.which("msedge"), shutil.which("chrome"),
                  r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                  r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                  r"C:\Program Files\Google\Chrome\Application\chrome.exe"]
    for exe in candidates:
        if exe and Path(exe).exists():
            subprocess.Popen([exe, f"--app={url}", "--window-size=1280,900"])
            return
    webbrowser.open(url)


def replace_running_copy():
    """Closing the app window doesn't stop its server, so an older copy may still be running
    (for example from before a `git pull`). Ask it to quit so this copy, with any updates, takes over."""
    try:
        quit_request = urllib.request.Request(f"http://127.0.0.1:{PORT}/api/quit", data=b"{}", method="POST",
                                              headers={"X-Kit": "1", "Content-Type": "application/json"})
        urllib.request.urlopen(quit_request, timeout=3)
    except OSError:
        pass  # very old copies don't know /api/quit
    for _ in range(20):
        try:
            return Server(("127.0.0.1", PORT), Handler)
        except OSError:
            time.sleep(0.25)
    return None


def restart():
    """Start the freshly downloaded version; it takes over from this copy via /api/quit."""
    # a new console only if we're running in one (the normal double-click case)
    flags = subprocess.CREATE_NEW_CONSOLE if os.name == "nt" and sys.stdout and sys.stdout.isatty() else 0
    subprocess.Popen([sys.executable, str(learn.ROOT / "app.py"), "--updated", "--no-window"],
                     cwd=learn.ROOT, creationflags=flags)


def main():
    if "--updated" not in sys.argv and updates.check():
        print("\n  Updating learn/programming...")
        ok, message = updates.apply()
        if ok:  # run the new version instead of this one
            sys.exit(subprocess.call([sys.executable, str(learn.ROOT / "app.py"), "--updated", *sys.argv[1:]]))
        print(f"  Couldn't update ({message}). Starting the current version.")
    url = f"http://127.0.0.1:{PORT}/"
    try:
        server = Server(("127.0.0.1", PORT), Handler)
    except OSError:
        server = replace_running_copy()
    if server is None:  # something else holds the port: show what's there
        print("\n  Another copy is running and wouldn't close. Close every learn/programming console window and try again.\n")
        return open_window(url)
    print(f"\n  learn/programming ({VERSION}) is running at {url}\n  Close this window to quit.\n")
    cloud.sync_in_background()  # catch up on anything finished while offline
    updates.check_in_background()
    if "--no-window" not in sys.argv:  # after an in-app update, the old window just reloads
        open_window(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
