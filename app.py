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
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import cloud
import learn
import updates

PORT = int(os.environ.get("LEARN_PORT", 8765))  # override only if 8765 is taken (or for testing)
HOSTS = {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}
VERSION = updates.version()
OPEN = {"/api/me", "/api/signin", "/api/signup", "/api/quit", "/api/ping"}  # everything else needs you signed in
LAST_SEEN = [time.time()]  # when the app window last talked to us
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
    return {**s, "missions": ms, "track": track, "logo": cfg.get("logo", ""),
            "errors": cfg.get("errors", {})}


def course_info(track, s, game_xp=0):
    cfg = learn.track_cfg(track)
    return {"track": track, "name": s["name"], "logo": cfg.get("logo", ""),
            "description": cfg.get("description", ""), "xp": s["xp"], "rank": s["rank"], "rank_xp": s["rank_xp"],
            "next": s["next"], "missions": [mission_info(track, m) for m in s["missions"]], "game_xp": game_xp}


def overview():
    """Every course's progress, plus a dated log of completed missions."""
    progress = learn.load_progress()
    games = progress.get("_games", {})
    courses = [course_info(track, learn.summary(track), games.get(track, {}).get("xp", 0)) for track in learn.tracks()]
    return {"courses": courses, "history": learn.history(progress), "checks": progress.get("_checks", {})}


def friend_overview(username):
    """Same shape as overview(), built from a friend's synced progress."""
    p = cloud.profile(username)
    finished = {}
    for c in p["completions"]:
        finished.setdefault(c["track"], []).append(c["mission_id"])
    readable = {(r["track"], r["mission_id"]) for r in p["readable"]}
    mine = learn.load_progress()
    game_xp = {g["track"]: g["xp"] for g in p["games"]}
    courses = []
    for track in learn.tracks():
        info = course_info(track, learn.summary(track, finished.get(track, [])), game_xp.get(track, 0))
        for m in info["missions"]:
            m["code"] = (track, m["id"]) in readable
            m["mine"] = m["id"] in mine.get(track, [])  # so the app can say "finish it" vs "not shared"
        courses.append(info)
    history = sorted(({"track": c["track"], "id": c["mission_id"], "date": c["completed_on"]} for c in p["completions"]),
                     key=lambda h: h["date"])
    return {"username": username, "avatar": p["avatar"], "joined": p["joined"], "courses": courses, "history": history,
            "checks": {a["day"]: a["checks"] for a in p["activity"]}}


def market():
    """The marketplace catalog, plus which courses you've added (and at which version)."""
    installed = {t: learn.installed_version(t) for t in learn.tracks()}
    try:
        courses, error = cloud.catalog(), None
    except cloud.CloudError as e:
        courses, error = [], str(e)  # offline: you can still use the courses you've added
    return {"courses": courses, "installed": installed, "error": error}


def current_streak(days):
    """Days in a row with activity, ending today or yesterday (ISO date strings)."""
    day, streak = date.today(), 0
    if day.isoformat() not in days:
        day -= timedelta(days=1)  # nothing yet today doesn't break yesterday's streak
    while day.isoformat() in days:
        streak, day = streak + 1, day - timedelta(days=1)
    return streak


def friends_view(details=True):
    """Friends with stats (XP, missions, streak, last active, rank per language), a feed of what they
    finished recently, and this week's XP for the leaderboard."""
    f = cloud.friends(details)
    week_start = (date.today() - timedelta(days=6)).isoformat()
    missions = {track: {m["id"]: m for m in learn.missions(track)} for track in learn.tracks()}
    feed = []
    for friend in f["friends"]:
        uid = friend.pop("id")
        done = [c for c in f["completions"] if c["user_id"] == uid and c["mission_id"] in missions.get(c["track"], {})]
        days = {c["completed_on"] for c in done} | {a["day"] for a in f["activity"] if a["user_id"] == uid}
        game_xp = sum(g["xp"] for g in f["games"] if g["user_id"] == uid)
        friend.update(xp=sum(c["xp"] for c in done) + game_xp, done=len(done), streak=current_streak(days),
                      week_xp=sum(c["xp"] for c in done if c["completed_on"] >= week_start),
                      last_active=max(days) if days else None, courses=[])
        for track in learn.tracks():
            ids = [c["mission_id"] for c in done if c["track"] == track]
            if ids:
                s = learn.summary(track, ids)
                friend["courses"].append({"name": s["name"], "rank": s["rank"], "done": len(ids), "total": len(s["missions"])})
        feed += [{"username": friend["username"], "avatar": friend["avatar"], "title": missions[c["track"]][c["mission_id"]]["title"],
                  "kind": missions[c["track"]][c["mission_id"]]["kind"], "course": learn.track_cfg(c["track"])["name"],
                  "xp": c["xp"], "date": c["completed_on"]} for c in done]
    progress = learn.load_progress()
    my_week = sum(m["xp"] for track in learn.tracks() for m in learn.missions(track)
                  for h in learn.history(progress) if h["track"] == track and h["id"] == m["id"] and h["date"] >= week_start)
    return {"friends": f["friends"], "incoming": f["incoming"], "outgoing": f["outgoing"],
            "feed": sorted(feed, key=lambda e: e["date"], reverse=True)[:40], "my_week_xp": my_week}


def games_view(track):
    """A course's games (Robot Maze levels, Bug Invaders lines, Code Racer snippets), your stats and friends' bests."""
    cfg = learn.track_cfg(track)
    try:
        friends = cloud.friend_games(track)
    except cloud.CloudError:
        friends = []  # offline: you can still play
    return {"track": track, "name": cfg["name"], "logo": cfg.get("logo", ""), "errors": cfg.get("errors", {}),
            **learn.games(track), "stats": learn.load_progress().get("_games", {}).get(track, {"xp": 0, "best": {}}),
            "friends": friends}


def play_robot(track, level_id, code):
    """Run a Robot Maze level. Stars: reach the flag on every world, grab every gem, and stay within par."""
    level = next((l for l in learn.games(track)["robot"] if l["id"] == level_id), None)
    if not level:
        raise ValueError("That level isn't in this course")
    report = learn.run_robot(track, level, code)
    maps = report["maps"]
    won = bool(maps) and all(m["won"] for m in maps)
    stars = won and 1 + all(m["gems"] == m["gems_total"] for m in maps) + (learn.code_lines(code) <= level["par"])
    report.update(won=won, stars=stars or 0, lines=learn.code_lines(code), xp=10 * stars if won else 0)
    if won:
        report["stats"] = learn.game_record(track, report["xp"], f"robot/{level_id}", stars)
        cloud.sync_in_background()
    return report


def game_xp(game, score):
    """XP for a finished Bug Invaders game (score) or Code Racer race (words per minute)."""
    return min(40, 5 + score // 250) if game == "invaders" else min(30, 5 + score // 10)


def me():
    s = cloud.session()
    if not s:
        return {"signed_in": False, "version": VERSION, "settings": learn.load_settings()}
    try:
        profile = cloud.my_profile()
    except cloud.CloudError:
        profile = {"avatar": None, "created_at": None}  # offline: show the letter instead
    return {"signed_in": True, "username": s["username"], "email": s["email"], "avatar": profile["avatar"],
            "joined": profile["created_at"], "sync": cloud.status,
            "version": VERSION, "update": updates.status, "settings": learn.load_settings()}


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
        if path.startswith("/api/") and self.headers.get("X-Kit") != "1":
            return False
        LAST_SEEN[0] = time.time()
        return True

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
            if url.path == "/api/market":
                return self.send(market())
            if url.path == "/api/realtime":  # party games: the window joins a Supabase Realtime room as you
                s = cloud.session()
                return self.send({"url": cloud.CONFIG["url"], "key": cloud.CONFIG["key"],
                                  "token": s["access_token"], "username": s["username"]})
            if url.path == "/api/games":
                if q.get("track") not in learn.tracks():
                    return self.send({"error": "unknown track"}, 400)
                return self.send(games_view(q["track"]))
            if url.path == "/api/ping":  # the open window checks in so we know it's still there
                return self.send({"update": updates.status["available"]})
            if url.path == "/api/friends":  # ?light=1: just requests, for the sidebar badge
                return self.send(friends_view(details=q.get("light") != "1"))
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
            if action in ("/api/market/add", "/api/market/remove"):
                course_id = body.get("id", "")
                if not learn.COURSE_ID.match(course_id):
                    return self.send({"error": "unknown course"}, 400)
                if action == "/api/market/add":  # also used for "Update": a fresh copy replaces the old one
                    version, files = cloud.download(course_id)
                    learn.install_course(course_id, version, files)
                else:
                    learn.remove_course(course_id)
                return self.send(market())
            if action.startswith("/api/game/") and body.get("track") not in learn.tracks():
                return self.send({"error": "unknown track"}, 400)
            if action == "/api/game/robot":  # run your Robot Maze code; the app animates the result
                code = body.get("code")
                if not isinstance(code, str) or len(code) > 20_000:
                    return self.send({"error": "bad game request"}, 400)
                return self.send(play_robot(body["track"], body.get("level"), code))
            if action == "/api/game/match":  # a finished party game with friends: XP, more for 1st and 2nd
                place, players = body.get("place"), body.get("players")
                if body.get("game") not in ("race", "blitz", "robot") or not isinstance(place, int) \
                        or not isinstance(players, int) or not 1 <= place <= players <= 8:
                    return self.send({"error": "bad game request"}, 400)
                xp = 10 + (players > 1) * {1: 25, 2: 10}.get(place, 0)
                won = place == 1 and players > 1
                wins = learn.load_progress().get("_games", {}).get(body["track"], {}).get("best", {}).get("party_wins", 0)
                stats = learn.game_record(body["track"], xp, "party_wins", wins + won)
                cloud.sync_in_background()
                return self.send({"xp": xp, "stats": stats})
            if action == "/api/game/score":  # a finished Bug Invaders game or Code Racer race
                game, score = body.get("game"), body.get("score")
                limit = {"invaders": 1_000_000, "racer": 400}.get(game)  # nobody types faster than ~300 WPM
                if not limit or not isinstance(score, int) or not 0 <= score <= limit:
                    return self.send({"error": "bad game request"}, 400)
                xp = game_xp(game, score)
                stats = learn.game_record(body["track"], xp, game, score)
                cloud.sync_in_background()
                return self.send({"xp": xp, "stats": stats})
            if action == "/api/settings":
                before = learn.load_settings()["share_code"]
                if learn.save_settings(body)["share_code"] != before:
                    cloud.sync_in_background()  # share or take down code right away
                return self.send(me())
            if action == "/api/password":
                cloud.change_password(body.get("password", ""))
                return self.send({"result": "changed"})
            if action == "/api/sync":
                cloud.sync()
                return self.send(me())
            if action == "/api/update/check":
                updates.check()
                return self.send(me())
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
        except (cloud.CloudError, ValueError) as e:
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
            opened = learn.load_settings()["open_vscode"] and learn.open_in_editor(target)
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


def quit_when_window_closed(server, timeout=180, every=15):
    """There's no console window to close, so stop once the app window has been gone for a while.
    (The window checks in every 30 seconds, even when minimized.)"""
    def watch():
        # count quiet checks rather than comparing clock times, so waking from sleep doesn't look like "gone for hours"
        seen, quiet = LAST_SEEN[0], 0
        while quiet * every < timeout:
            time.sleep(every)
            quiet = 0 if LAST_SEEN[0] != seen else quiet + 1
            seen = LAST_SEEN[0]
        server.shutdown()
    threading.Thread(target=watch, daemon=True).start()


def log_to_file():
    """Without a console (pythonw), send messages and errors to workspace/app.log instead."""
    if sys.stdout is None or sys.stderr is None:
        learn.WORK.mkdir(parents=True, exist_ok=True)
        log = open(learn.WORK / "app.log", "a", encoding="utf-8", buffering=1)
        sys.stdout = sys.stderr = log
        print(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} starting")


def main():
    log_to_file()
    learn.seed_courses()  # courses you already had progress in, from before the marketplace
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
    updates.check_in_background()  # first check right away, without making the window wait for GitHub
    quit_when_window_closed(server)
    if "--no-window" not in sys.argv:  # after an in-app update, the old window just reloads
        open_window(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
