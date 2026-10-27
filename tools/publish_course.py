"""Publish a course folder (tracks/<id>) to the marketplace.

Usage: python tools/publish_course.py <course id>
Uses your signed-in session (sign in to the app first). Only publisher accounts are allowed;
the database refuses everyone else. Publishing bumps the course's version, so everyone who
added the course sees "Update".
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import cloud  # noqa: E402  (needs ROOT on the path first)

SAFE_PATH = re.compile(r"^[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)*$")
BATCH = 40  # files per upload request


def course_files(folder):
    for f in sorted(folder.rglob("*")):
        rel = f.relative_to(folder).as_posix()
        if f.is_dir() or "__pycache__" in rel or f.suffix == ".pyc":
            continue
        if not SAFE_PATH.match(rel) or ".." in rel.split("/"):
            sys.exit(f"Unsafe file name, rename it first: {rel}")
        yield {"path": rel, "content": f.read_text(encoding="utf-8")}


def rpc(name, **args):
    return cloud._rest("POST", f"rpc/{name}", args)


def main(course_id):
    if not cloud.session():
        sys.exit("Sign in to the app first.")
    folder = ROOT / "tracks" / course_id
    cfg = json.loads((folder / "track.json").read_text(encoding="utf-8"))
    missions = [json.loads(m.read_text(encoding="utf-8")) for m in sorted(folder.glob("*/mission.json"))]
    info = {"name": cfg["name"], "description": cfg.get("description", ""), "logo": cfg.get("logo", ""),
            "missions": len(missions), "chapters": list(dict.fromkeys(m.get("chapter", "") for m in missions))}
    files = list(course_files(folder))
    rpc("begin_publish", course=course_id, info=info)  # hides the course while it uploads
    for i in range(0, len(files), BATCH):
        rpc("publish_course_files", course=course_id, files=files[i:i + BATCH])
        print(f"  uploaded {min(i + BATCH, len(files))}/{len(files)} files")
    version = rpc("finish_publish", course=course_id)
    fingerprint = hashlib.sha256("".join(f["path"] + f["content"] for f in files).encode()).hexdigest()[:12]
    print(f"{course_id} v{version} published: {len(missions)} missions, {len(files)} files (fingerprint {fingerprint})")


if __name__ == "__main__":
    main(sys.argv[1])
