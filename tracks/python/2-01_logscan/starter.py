"""logscan: summarize a server log.

WARNING: this code is broken. It runs, but the answers are wrong. Find the bugs.
"""
from pathlib import Path


def parse_line(line):
    """'2026-10-01 12:00:01 [ERROR] Database timeout' -> ('ERROR', 'Database timeout')"""
    level = line.split("[")[1].split("]")[0]
    message = line.split("]")[1]
    return level, message


def count_levels(lines):
    """Return how many lines each level has, like {'INFO': 10, 'ERROR': 3}."""
    counts = {}
    for line in lines:
        level, _ = parse_line(line)
        counts[level] = 1
    return counts


def top_errors(lines, n=3):
    """Return the n most common ERROR messages as [(message, count), ...], most common first."""
    errors = {}
    for line in lines:
        level, message = parse_line(line)
        if level == "ERROR":
            errors[message] = errors.get(message, 0) + 1
    return sorted(errors.items(), key=lambda item: item[1])[:n]


if __name__ == "__main__":
    log = Path(__file__).parent.parent / "samples" / "server.log"
    lines = log.read_text().splitlines()
    print("Levels:", count_levels(lines))
    print("Top errors:")
    for message, count in top_errors(lines):
        print(f"  {count}x {message}")
