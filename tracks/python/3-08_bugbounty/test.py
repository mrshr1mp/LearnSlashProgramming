import importlib.util
import re
from pathlib import Path
from types import SimpleNamespace


def load_real():
    spec = importlib.util.spec_from_file_location("textkit_real", Path(__file__).parent / "samples" / "textkit.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


REAL = load_real()


def duration(text, pattern=r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", match=re.fullmatch, check_empty=True, units=(3600, 60, 1)):
    m = match(pattern, text)
    if (check_empty and not text) or not m:
        raise ValueError(f"bad duration: {text!r}")
    return sum(int(g or 0) * u for g, u in zip(m.groups(), units))


def mutant(**overrides):
    return SimpleNamespace(**{"slugify": REAL.slugify, "clamp": REAL.clamp, "parse_duration": REAL.parse_duration, **overrides})


# (hint shown if nobody catches it, broken module)
BUGS = [
    ("slugify: something about upper-case letters",
     mutant(slugify=lambda t: re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-"))),
    ("slugify: something about the start and end of the slug",
     mutant(slugify=lambda t: re.sub(r"[^a-z0-9]+", "-", t.lower()))),
    ("slugify: something about several symbols in a row",
     mutant(slugify=lambda t: re.sub(r"[^a-z0-9]", "-", t.lower()).strip("-"))),
    ("clamp: something about numbers above the range",
     mutant(clamp=lambda x, low, high: low if x < low else low if x > high else x)),
    ("clamp: something about numbers below the range",
     mutant(clamp=lambda x, low, high: min(x, high))),
    ("parse_duration: something about one of the units",
     mutant(parse_duration=lambda t: duration(t, units=(3600, 60, 0)))),
    ("parse_duration: something about empty input",
     mutant(parse_duration=lambda t: duration(t, check_empty=False))),
    ("parse_duration: something about text that isn't a duration",
     mutant(parse_duration=lambda t: duration(t, match=re.match))),
]


def user_tests(sol):
    return [(name, fn) for name, fn in vars(sol).items() if name.startswith("test_") and callable(fn)]


def failures(sol, module):
    failed = []
    for name, fn in user_tests(sol):
        try:
            fn(module)
        except Exception as e:
            failed.append(f"{name}: {type(e).__name__} {e}".strip())
    return failed


def test_you_wrote_tests(sol):
    n = len(user_tests(sol))
    assert n >= 3, f"write at least 3 test_ functions (found {n})"


def test_all_pass_on_real_textkit(sol):
    failed = failures(sol, REAL)
    assert not failed, "these tests FAIL on the real, correct textkit, so the test itself is wrong:\n          " + \
        "\n          ".join(failed)


def catches(i, hint, broken):
    def test(sol):
        assert failures(sol, broken), f"none of your tests caught this bug yet. Hint: {hint}"
    return test


for _i, (_hint, _broken) in enumerate(BUGS, 1):
    globals()[f"test_catches_bug_{_i}"] = catches(_i, _hint, _broken)
