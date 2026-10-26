"""Accounts, progress sync and friends, backed by Supabase.

cloud.json only holds the *publishable* key, which is meant to be public: what each signed-in
user can read or write is decided by the database's row-level security rules (supabase/schema.sql).
Your login session is stored in workspace/session.json, which git ignores.
"""
import json
import re
import threading
import time
import urllib.error
import urllib.request
from urllib.parse import quote

import learn

CONFIG = json.loads((learn.ROOT / "cloud.json").read_text(encoding="utf-8"))
SESSION = learn.WORK / "session.json"
USERNAME = re.compile(r"^[A-Za-z0-9_]{3,20}$")
MAX_CODE = 100_000  # bytes, same limit as the database
status = {"synced_at": None, "error": None}


class CloudError(Exception):
    def __init__(self, message, offline=False):
        super().__init__(message)
        self.offline = offline


def _request(method, path, body=None, token=None, prefer=None):
    headers = {"apikey": CONFIG["key"], "Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if prefer:
        headers["Prefer"] = prefer
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(CONFIG["url"] + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode()
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode())
            message = err.get("msg") or err.get("message") or err.get("error_description") or err.get("error")
        except ValueError:
            message = None
        raise CloudError(message or f"Server error {e.code}") from None
    except (urllib.error.URLError, TimeoutError):
        raise CloudError("Can't reach the server. Are you online?", offline=True) from None
    return json.loads(text) if text else None


# ---------- accounts ----------
def _save_session(auth):
    user = auth["user"]
    s = {"access_token": auth["access_token"], "refresh_token": auth["refresh_token"],
         "expires_at": time.time() + auth["expires_in"] - 60, "user_id": user["id"], "email": user["email"],
         "username": (user.get("user_metadata") or {}).get("username")}
    SESSION.parent.mkdir(parents=True, exist_ok=True)
    SESSION.write_text(json.dumps(s))
    return s


def session():
    """The current login, refreshed if it expired. None when signed out."""
    if not SESSION.exists():
        return None
    s = json.loads(SESSION.read_text())
    if time.time() > s["expires_at"]:
        try:
            s = _save_session(_request("POST", "/auth/v1/token?grant_type=refresh_token", {"refresh_token": s["refresh_token"]}))
        except CloudError as e:
            if e.offline:
                return s  # keep you signed in; calls will just fail until you're back online
            SESSION.unlink(missing_ok=True)
            return None
    return s


def sign_up(email, password, username):
    if not USERNAME.match(username or ""):
        raise CloudError("Usernames are 3-20 letters, numbers or _")
    if not _request("POST", "/rest/v1/rpc/username_available", {"name": username}):
        raise CloudError(f"The username {username} is taken")
    auth = _request("POST", "/auth/v1/signup", {"email": email, "password": password, "data": {"username": username}})
    if not auth or "access_token" not in auth:
        raise CloudError("Account created, but the server wants an email confirmation first. "
                         "Turn off 'Confirm email' in Supabase (see README), then sign in.")
    return _save_session(auth)


def sign_in(email, password):
    return _save_session(_request("POST", "/auth/v1/token?grant_type=password", {"email": email, "password": password}))


def sign_out():
    s = session()
    if s:
        try:
            _request("POST", "/auth/v1/logout", {}, s["access_token"])
        except CloudError:
            pass
    SESSION.unlink(missing_ok=True)


def _rest(method, path, body=None, prefer=None):
    s = session()
    if not s:
        raise CloudError("You're signed out")
    return _request(method, "/rest/v1/" + path, body, s["access_token"], prefer)


# ---------- syncing your progress ----------
def sync():
    """Upload your finished missions, daily checks and code for finished missions. Safe to repeat."""
    s = session()
    if not s:
        return
    progress = learn.load_progress()
    dates = {(h["track"], h["id"]): h["date"] for h in learn.history(progress)}
    completions, solutions = [], []
    for track in learn.tracks():
        for m in learn.missions(track):
            if m["id"] not in progress.get(track, []):
                continue
            key = {"user_id": s["user_id"], "track": track, "mission_id": m["id"]}
            completions.append({**key, "xp": m["xp"], "completed_on": dates[(track, m["id"])]})
            f = learn.WORK / track / m["file"]
            if f.exists() and f.stat().st_size <= MAX_CODE:
                solutions.append({**key, "filename": f.name, "code": f.read_text(encoding="utf-8", errors="replace")})
    activity = [{"user_id": s["user_id"], "day": day, "checks": n} for day, n in progress.get("_checks", {}).items()]
    upsert = "resolution=merge-duplicates,return=minimal"
    for table, rows in [("completions", completions), ("solutions", solutions), ("activity", activity)]:
        if rows:  # completions first: code can only be uploaded for finished missions
            _rest("POST", table, rows, upsert)
    status.update(synced_at=time.time(), error=None)


def sync_in_background():
    def run():
        try:
            sync()
        except CloudError as e:
            status["error"] = str(e)
    threading.Thread(target=run, daemon=True).start()


# ---------- friends ----------
def _ids_in(ids):
    return "(" + ",".join(ids) + ")"


def friends():
    """Accepted friends with their XP, plus incoming and outgoing requests."""
    me = session()["user_id"]
    rows = _rest("GET", "friendships?select=requester,addressee,status")
    others = {r["requester"] if r["addressee"] == me else r["addressee"] for r in rows}
    names = {p["id"]: p["username"] for p in _rest("GET", f"profiles?select=id,username&id=in.{_ids_in(others)}")} if others else {}
    accepted = [r["requester"] if r["addressee"] == me else r["addressee"] for r in rows if r["status"] == "accepted"]
    xp = {}
    if accepted:
        for c in _rest("GET", f"completions?select=user_id,xp&user_id=in.{_ids_in(accepted)}"):
            xp[c["user_id"]] = xp.get(c["user_id"], 0) + c["xp"]
    return {
        "friends": [{"username": names[i], "xp": xp.get(i, 0)} for i in accepted if i in names],
        "incoming": [names[r["requester"]] for r in rows if r["status"] == "pending" and r["addressee"] == me and r["requester"] in names],
        "outgoing": [names[r["addressee"]] for r in rows if r["status"] == "pending" and r["requester"] == me and r["addressee"] in names],
    }


def add_friend(username):
    return _rest("POST", "rpc/send_friend_request", {"target": username})


def accept_friend(username):
    _rest("POST", "rpc/accept_friend", {"requester_name": username})


def _user_id(username):
    rows = _rest("GET", f"profiles?select=id&username=eq.{quote(username)}")
    if not rows:
        raise CloudError(f"{username} isn't your friend")
    return rows[0]["id"]


def remove_friend(username):
    me, them = session()["user_id"], _user_id(username)
    _rest("DELETE", f"friendships?or=(and(requester.eq.{me},addressee.eq.{them}),and(requester.eq.{them},addressee.eq.{me}))")


def profile(username):
    """A friend's finished missions and activity. The database only answers for accepted friends."""
    uid = _user_id(username)
    return {
        "completions": _rest("GET", f"completions?select=track,mission_id,completed_on&user_id=eq.{uid}"),
        "activity": _rest("GET", f"activity?select=day,checks&user_id=eq.{uid}"),
        # only lists missions whose code you're allowed to see (ones you've finished too)
        "readable": _rest("GET", f"solutions?select=track,mission_id&user_id=eq.{uid}"),
    }


def code(username, track, mission_id):
    rows = _rest("GET", f"solutions?select=filename,code&user_id=eq.{_user_id(username)}"
                        f"&track=eq.{quote(track)}&mission_id=eq.{quote(mission_id)}")
    if not rows:
        raise CloudError("Finish this mission yourself to see their code")
    return rows[0]
