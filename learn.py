"""Mission control. Run `python learn.py` to see your missions (or `python app.py` for the app)."""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "tracks"           # course sources, published to the marketplace with tools/publish_course.py
WORK = ROOT / "workspace"
TRACKS = WORK / "courses"          # the courses you've added from the marketplace
PROGRESS = WORK / "progress.json"
COURSE_ID = re.compile(r"^[a-z0-9_-]{1,40}$")
SAFE_PATH = re.compile(r"^[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)*$")


def tracks():
    """The courses you've added (an empty list until you add one from the marketplace)."""
    if not TRACKS.exists():
        return []
    return sorted(d.name for d in TRACKS.iterdir() if not d.name.startswith(".") and (d / "track.json").exists())


def installed_version(course_id):
    f = TRACKS / course_id / ".version"
    return int(f.read_text()) if f.exists() else None


def install_course(course_id, version, files):
    """Write a downloaded course into workspace/courses/<id>, replacing any older copy.
    Every file path is checked, so a course can never write outside its own folder."""
    if not COURSE_ID.match(course_id) or course_id == "courses":
        raise ValueError(f"Bad course id: {course_id!r}")
    if not any(f["path"] == "track.json" for f in files):
        raise ValueError("That course download is incomplete (no track.json)")
    TRACKS.mkdir(parents=True, exist_ok=True)
    temp = TRACKS / f".download-{course_id}"
    shutil.rmtree(temp, ignore_errors=True)
    for f in files:
        path = f["path"]
        target = (temp / path).resolve()
        if not SAFE_PATH.match(path) or ".." in path.split("/") or temp.resolve() not in target.parents:
            shutil.rmtree(temp, ignore_errors=True)
            raise ValueError(f"Refused an unsafe file in the course: {path!r}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f["content"], encoding="utf-8")
    (temp / ".version").write_text(str(version))
    final = TRACKS / course_id
    shutil.rmtree(final, ignore_errors=True)  # only the course files: your code and progress live elsewhere
    temp.rename(final)


def remove_course(course_id):
    """Remove a course's files. Your code and progress for it stay, so adding it back picks up where you left off."""
    if COURSE_ID.match(course_id):
        shutil.rmtree(TRACKS / course_id, ignore_errors=True)


def seed_courses():
    """Courses you already have progress in (from before the marketplace) get added automatically,
    from the copy that ships with the app. Version 0 means "update from the marketplace when you like"."""
    progress = load_progress()
    for course_id in progress:
        src = SOURCE / course_id
        if not course_id.startswith("_") and (src / "track.json").exists() and course_id not in tracks():
            shutil.copytree(src, TRACKS / course_id, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (TRACKS / course_id / ".version").write_text("0")


def track_cfg(track):
    return json.loads((TRACKS / track / "track.json").read_text(encoding="utf-8"))


def missions(track):
    dirs = sorted(d for d in (TRACKS / track).iterdir() if (d / "mission.json").exists())
    return [dict(json.loads((d / "mission.json").read_text(encoding="utf-8")), id=d.name, dir=d, n=i)
            for i, d in enumerate(dirs, 1)]


def load_progress():
    return json.loads(PROGRESS.read_text()) if PROGRESS.exists() else {}


def save_progress(progress):
    PROGRESS.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS.write_text(json.dumps(progress, indent=2))


SETTINGS = WORK / "settings.json"
DEFAULT_SETTINGS = {"accent": "red", "background": "dark", "sound": True, "confetti": True, "reduce_motion": False,
                    "open_vscode": True, "share_code": True}
CHOICES = {"accent": {"red", "orange", "gold", "green", "blue", "purple", "pink"}, "background": {"dark", "black"}}


def load_settings():
    saved = json.loads(SETTINGS.read_text()) if SETTINGS.exists() else {}
    return {**DEFAULT_SETTINGS, **{k: v for k, v in saved.items() if k in DEFAULT_SETTINGS}}


def save_settings(changes):
    """Apply only known settings with allowed values; anything else is ignored."""
    settings = load_settings()
    for key, value in changes.items():
        if key in CHOICES and value in CHOICES[key] or key in DEFAULT_SETTINGS and key not in CHOICES and isinstance(value, bool):
            settings[key] = value
    SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS.write_text(json.dumps(settings, indent=2))
    return settings


def summary(track, done=None):
    """XP, rank and mission statuses. `done` defaults to your own finished missions (pass a friend's instead)."""
    cfg = track_cfg(track)
    mine = done is None
    done = load_progress().get(track, []) if mine else done
    ms = missions(track)
    xp = sum(m["xp"] for m in ms if m["id"] in done)
    reached = [r for r in cfg["ranks"] if xp >= r[0]]
    upcoming = [r for r in cfg["ranks"] if xp < r[0]]
    in_chapter = {}
    for m in ms:
        started = mine and (WORK / track / m["file"]).exists()
        m["status"] = "done" if m["id"] in done else "started" if started else "new"
        m.setdefault("chapter", "")
        in_chapter[m["chapter"]] = m["chapter_n"] = in_chapter.get(m["chapter"], 0) + 1
    return {"name": cfg["name"], "xp": xp, "rank": reached[-1][1], "rank_xp": reached[-1][0],
            "next": upcoming[0] if upcoming else None, "missions": ms}


def history(progress):
    """Dated list of finished missions. Ones finished before dates were logged use the file's last save."""
    logged = progress.get("_history", [])
    seen = {(h["track"], h["id"]) for h in logged}
    extra = []
    for track in tracks():
        for m in missions(track):
            if m["id"] in progress.get(track, []) and (track, m["id"]) not in seen:
                f = WORK / track / m["file"]
                day = date.fromtimestamp(f.stat().st_mtime) if f.exists() else date.today()
                extra.append({"track": track, "id": m["id"], "date": day.isoformat()})
    return sorted(logged + extra, key=lambda h: h["date"])


def prepare(track, m):
    """Copy the starter and samples into the workspace. Never overwrites the learner's code."""
    ws = WORK / track
    target = ws / m["file"]
    target.parent.mkdir(parents=True, exist_ok=True)
    starter = next(m["dir"].glob("starter.*"), None)
    if not target.exists():
        shutil.copy(starter, target) if starter else target.touch()
    if (m["dir"] / "samples").exists():
        shutil.copytree(m["dir"] / "samples", ws / "samples", dirs_exist_ok=True)
    return target


def run_tests(track, m):
    """Return (passed, output) from running the mission's tests on the learner's file."""
    return _run(track, next(m["dir"].glob("test.*")), WORK / track / m["file"], WORK / track, timeout=60)


def _run(track, test, solution, cwd, timeout):
    cmd = [arg.format(python=sys.executable, track=TRACKS / track, test=test, solution=solution)
           for arg in track_cfg(track)["run"]]
    try:
        r = subprocess.run(cmd, cwd=cwd, timeout=timeout, capture_output=True, encoding="utf-8",
                           errors="replace", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    except subprocess.TimeoutExpired:
        return False, f"Your code ran for over {timeout} seconds. Infinite loop?"
    return r.returncode == 0, r.stdout + r.stderr


# ---------- games ----------
GAME_XP = {"bug": 10, "speed": 10, "golf": 15}  # per challenge solved
ROUND_XP = 20                                   # bonus for finishing a Bug Squash or Speed Run round


def games(track):
    """The course's game challenges, from games/*.game: `key: value` lines, a blank line, the task,
    then `=== starter`, `=== test` and optionally `=== broken` (Bug Squash) sections. `golf: N` is the par."""
    out = []
    for f in sorted((TRACKS / track / "games").glob("*.game")):
        head, *sections = re.split(r"^=== (\w+)\n", f.read_text(encoding="utf-8"), flags=re.M)
        meta, _, task = head.partition("\n\n")
        g = dict(line.split(": ", 1) for line in meta.splitlines())
        out.append({**g, "id": f.stem, "task": task.strip(), "golf": int(g["golf"]) if "golf" in g else None,
                    **dict(zip(sections[::2], sections[1::2]))})
    return out


def run_game(track, g, code):
    """Test code typed into a game. Returns (passed, output, the file the code was saved to)."""
    ws = WORK / track / "games"
    ws.mkdir(parents=True, exist_ok=True)
    test, solution = ws / "game_test.py", ws / "game.py"
    test.write_text(g["test"], encoding="utf-8")
    solution.write_text(code, encoding="utf-8")
    return (*_run(track, test, solution, ws, timeout=10), solution)


def game_record(track, xp, key=None, score=None):
    """Add game XP and keep your best (lowest) score under `key`. Returns this course's game stats."""
    progress = load_progress()
    stats = progress.setdefault("_games", {}).setdefault(track, {"xp": 0, "best": {}})
    stats["xp"] += xp
    new_best = key is not None and (key not in stats["best"] or score < stats["best"][key])
    if new_best:
        stats["best"][key] = score
    save_progress(progress)
    return {**stats, "new_best": new_best}


def log_check():
    """Count one check run toward today's activity (the dashboard heatmap)."""
    progress = load_progress()
    checks = progress.setdefault("_checks", {})
    today = date.today().isoformat()
    checks[today] = checks.get(today, 0) + 1
    save_progress(progress)


def award(track, m):
    """Mark the mission done and log the date. Returns True the first time."""
    progress = load_progress()
    done = progress.setdefault(track, [])
    if m["id"] in done:
        return False
    done.append(m["id"])
    progress.setdefault("_history", []).append({"track": track, "id": m["id"], "date": date.today().isoformat()})
    save_progress(progress)
    return True


def open_in_editor(target, line=None):
    """Open the project in VS Code at the learner's file. Returns False if VS Code isn't on PATH."""
    code = shutil.which("code")
    if code:
        subprocess.Popen([code, str(ROOT), "-g", f"{target}:{line}" if line else str(target)])
    return bool(code)


def status(track):
    s = summary(track)
    print(f"\n  {s['name']} track    XP {s['xp']}    rank: {s['rank']}\n")
    marks = {"done": "[x]", "started": "[>]", "new": "[ ]"}
    chapter = None
    for m in s["missions"]:
        if m["chapter"] != chapter:
            chapter = m["chapter"]
            print(f"\n  -- {chapter} --")
        print(f"  {marks[m['status']]} {m['n']:>2}. {m['title']:<26} {m['kind']:<7} {m['xp']:>4} xp")
    print("\n  python learn.py start N    open mission N")
    print("  python learn.py check N    run the tests on your code\n")


def main():
    p = argparse.ArgumentParser(description="Learn to code by building things.")
    p.add_argument("action", nargs="?", choices=["start", "check"])
    p.add_argument("mission", nargs="?", type=int, help="mission number")
    p.add_argument("--track", default="python", help="which language track (folder in tracks/)")
    args = p.parse_args()
    seed_courses()
    if args.track not in tracks():
        sys.exit(f"  You haven't added the {args.track} course. Add it from the Marketplace in the app.")
    if not args.action:
        return status(args.track)
    ms = missions(args.track)
    if not args.mission or not 1 <= args.mission <= len(ms):
        sys.exit(f"  Pick a mission number from 1 to {len(ms)}.")
    m = ms[args.mission - 1]
    if args.action == "start":
        target = prepare(args.track, m)
        print(f"\n  {m['title']}\n  brief: {m['dir'] / 'mission.md'}\n  code:  {target}\n")
        if load_settings()["open_vscode"]:
            open_in_editor(target)
        return
    if not (WORK / args.track / m["file"]).exists():
        sys.exit(f"  Start the mission first: python learn.py start {m['n']}")
    print(f"\n  Checking {m['title']}...\n")
    log_check()
    passed, output = run_tests(args.track, m)
    print(output)
    if not passed:
        print("  Not yet. Fix the FIRST problem above, then check again.\n")
        return
    print(f"  *** MISSION COMPLETE  +{m['xp']} xp ***" if award(args.track, m) else "  Still passing.")
    status(args.track)


if __name__ == "__main__":
    main()
