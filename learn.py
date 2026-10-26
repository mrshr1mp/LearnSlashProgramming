"""Mission control. Run `python learn.py` to see your missions (or `python app.py` for the app)."""
import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
TRACKS = ROOT / "tracks"
WORK = ROOT / "workspace"
PROGRESS = WORK / "progress.json"


def tracks():
    return sorted(d.name for d in TRACKS.iterdir() if (d / "track.json").exists())


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
    ws = WORK / track
    paths = dict(python=sys.executable, track=TRACKS / track, test=next(m["dir"].glob("test.*")),
                 solution=ws / m["file"])
    cmd = [arg.format(**paths) for arg in track_cfg(track)["run"]]
    try:
        r = subprocess.run(cmd, cwd=ws, timeout=60, capture_output=True, encoding="utf-8", errors="replace",
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    except subprocess.TimeoutExpired:
        return False, "Your code ran for over 60 seconds. Infinite loop?"
    return r.returncode == 0, r.stdout + r.stderr


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
    if not args.action:
        return status(args.track)
    ms = missions(args.track)
    if not args.mission or not 1 <= args.mission <= len(ms):
        sys.exit(f"  Pick a mission number from 1 to {len(ms)}.")
    m = ms[args.mission - 1]
    if args.action == "start":
        target = prepare(args.track, m)
        print(f"\n  {m['title']}\n  brief: {m['dir'] / 'mission.md'}\n  code:  {target}\n")
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
