"""textkit: three small, correct functions. Write tests that prove it."""
import re


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def clamp(x, low, high):
    return max(low, min(x, high))


def parse_duration(text):
    m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", text)
    if not text or not m:
        raise ValueError(f"bad duration: {text!r}")
    h, mins, s = (int(g or 0) for g in m.groups())
    return h * 3600 + mins * 60 + s
