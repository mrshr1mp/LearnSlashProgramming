import hashlib
import tempfile
from pathlib import Path

from harness import eq

FILES = {"a.txt": "hello", "sub/b.txt": "hello", "sub/deep/c.txt": "hello",
         "d.txt": "world", "e.txt": "unique", "f.bin": "world", "sub/g.txt": "Hello"}


def tree():
    tmp = Path(tempfile.mkdtemp())
    for name, text in FILES.items():
        (tmp / name).parent.mkdir(parents=True, exist_ok=True)
        (tmp / name).write_text(text)
    return tmp


def test_file_hash(sol):
    tmp = tree()
    eq(sol.file_hash(tmp / "a.txt"), hashlib.sha256(b"hello").hexdigest(), "file_hash of a file containing 'hello'")
    big = tmp / "big.bin"
    big.write_bytes(bytes(range(256)) * 1000)
    eq(sol.file_hash(big), hashlib.sha256(bytes(range(256)) * 1000).hexdigest(), "file_hash of a 256 KB file")


def test_walk_files_is_generator(sol):
    result = sol.walk_files(tree())
    assert iter(result) is result, f"walk_files should be a generator (use yield), but it returned a {type(result).__name__}"


def test_walk_files(sol):
    tmp = tree()
    got = sorted(Path(p).relative_to(tmp).as_posix() for p in sol.walk_files(tmp))
    eq(got, sorted(FILES), "files found by walk_files (folders should not be included)")


def test_find_dupes(sol):
    tmp = tree()
    want = [[tmp / "a.txt", tmp / "sub/b.txt", tmp / "sub/deep/c.txt"], [tmp / "d.txt", tmp / "f.bin"]]
    got = [[Path(p) for p in group] for group in sol.find_dupes(tmp)]
    eq(got, want, "find_dupes (note 'Hello' with a capital H is different)")
