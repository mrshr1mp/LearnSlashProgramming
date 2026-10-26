import subprocess
import sys
import tempfile
from pathlib import Path

from harness import eq

PATH_ONLY = True  # this mission is tested by running `python -m kit`, not by importing it


def kit(main_path, *args):
    cwd = Path(main_path).parent.parent
    return subprocess.run([sys.executable, "-m", "kit", *map(str, args)], cwd=cwd,
                          capture_output=True, text=True, timeout=30)


def lines(result):
    assert result.returncode == 0, f"exit code {result.returncode}. Error output:\n{result.stderr}"
    return result.stdout.strip().splitlines()


def test_help(path):
    r = kit(path, "--help")
    out = r.stdout.lower()
    assert r.returncode == 0, f"--help should exit with code 0, got {r.returncode}\n{r.stderr}"
    for cmd in ["logscan", "words", "organize", "dupes"]:
        assert cmd in out, f"--help output should mention '{cmd}'. It printed:\n{r.stdout}"


def test_unknown_command(path):
    r = kit(path, "make-me-a-sandwich")
    assert r.returncode != 0, "an unknown command should exit with a non-zero code"


def test_logscan(path):
    log = Path(tempfile.mkdtemp()) / "test.log"
    log.write_text("2026-10-01 00:00:01 [INFO] a\n2026-10-01 00:00:02 [ERROR] b\n\n"
                   "2026-10-01 00:00:03 [WARN] c\n2026-10-01 00:00:04 [ERROR] d\n2026-10-01 00:00:05 [INFO] e\n"
                   "2026-10-01 00:00:06 [ERROR] f\n")
    eq(lines(kit(path, "logscan", log)), ["ERROR: 3", "INFO: 2", "WARN: 1"], "logscan output")


def test_words(path):
    text = Path(tempfile.mkdtemp()) / "t.txt"
    text.write_text("b a c a b a")
    eq(lines(kit(path, "words", text, "--top", "2")), ["a 3", "b 2"], "words --top 2 output")
    eq(lines(kit(path, "words", text)), ["a 3", "b 2", "c 1"], "words output (default top 10)")


def test_organize(path):
    tmp = Path(tempfile.mkdtemp())
    for name in ["b.mp3", "a.png", "c.zip"]:
        (tmp / name).write_text(name)
    want = ["a.png -> images", "b.mp3 -> audio", "c.zip -> other"]
    eq(lines(kit(path, "organize", tmp)), want, "organize output (dry run)")
    assert (tmp / "a.png").exists(), "organize without --go must not move files"
    eq(lines(kit(path, "organize", tmp, "--go")), want + ["moved 3 files"], "organize --go output")
    assert (tmp / "images" / "a.png").exists(), "organize --go should move a.png into images/"


def test_dupes(path):
    tmp = Path(tempfile.mkdtemp())
    for name, text in {"x.txt": "same", "y.txt": "same", "z.txt": "other"}.items():
        (tmp / name).write_text(text)
    out = lines(kit(path, "dupes", tmp))
    eq([Path(p).name for p in out], ["x.txt", "y.txt"], "dupes output (file names)")
    (tmp / "y.txt").unlink()
    eq(lines(kit(path, "dupes", tmp)), ["no duplicates"], "dupes output with no duplicates")
