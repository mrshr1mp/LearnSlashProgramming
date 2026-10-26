import tempfile
from pathlib import Path

from harness import eq

FILES = ["PARTY.JPG", "essay.pdf", "beat.mp3", "game.py", "weird.xyz", "README", "photo.png"]
WANT = {"PARTY.JPG": "images", "essay.pdf": "docs", "beat.mp3": "audio", "game.py": "code",
        "weird.xyz": "other", "README": "other", "photo.png": "images"}


def messy_folder():
    tmp = Path(tempfile.mkdtemp())
    for name in FILES:
        (tmp / name).write_text(name)
    (tmp / "already_a_folder").mkdir()
    return tmp


def test_plan(sol):
    eq(sol.plan(messy_folder()), WANT, "plan() (folders should be skipped)")


def test_plan_moves_nothing(sol):
    tmp = messy_folder()
    sol.plan(tmp)
    sol.organize(tmp)  # dry_run defaults to True
    eq(sorted(p.name for p in tmp.iterdir() if p.is_file()), sorted(FILES), "files left in place after plan() and a dry run")


def test_organize_moves(sol):
    tmp = messy_folder()
    eq(sol.organize(tmp, dry_run=False), WANT, "organize(dry_run=False) return value")
    for name, folder in WANT.items():
        assert (tmp / folder / name).exists(), f"{name} should have been moved to {folder}/"
        assert not (tmp / name).exists(), f"{name} is still in the top folder"
    assert (tmp / "already_a_folder").is_dir(), "already_a_folder should be left alone"


def test_never_overwrite(sol):
    tmp = messy_folder()
    (tmp / "images").mkdir()
    (tmp / "images" / "photo.png").write_text("the OLD photo")
    sol.organize(tmp, dry_run=False)
    eq((tmp / "images" / "photo.png").read_text(), "the OLD photo", "existing images/photo.png must not be overwritten")
    renamed = tmp / "images" / "photo (1).png"
    assert renamed.exists(), "the new photo.png should be saved as images/photo (1).png"
    eq(renamed.read_text(), "photo.png", "contents of images/photo (1).png")


def test_run_twice(sol):
    tmp = messy_folder()
    sol.organize(tmp, dry_run=False)
    eq(sol.plan(tmp), {}, "plan() on an already-organized folder")
