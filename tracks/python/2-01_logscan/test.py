from harness import eq

LINES = [
    "2026-10-01 12:00:01 [INFO] Server started\n",
    "2026-10-01 12:00:02 [ERROR] Database timeout\n",
    "\n",
    "2026-10-01 12:00:03 [ERROR] Database timeout\n",
    "2026-10-01 12:00:04 [WARN] Disk 91% full\n",
    "2026-10-01 12:00:05 [ERROR] User not found\n",
    "   \n",
    "2026-10-01 12:00:06 [INFO] Request served\n",
]


def test_parse_line(sol):
    eq(sol.parse_line(LINES[1]), ("ERROR", "Database timeout"), "parse_line on an ERROR line")
    eq(sol.parse_line(LINES[4]), ("WARN", "Disk 91% full"), "parse_line on a WARN line")


def test_count_levels(sol):
    eq(sol.count_levels(LINES), {"INFO": 2, "ERROR": 3, "WARN": 1}, "count_levels (log has blank lines)")


def test_top_errors(sol):
    eq(sol.top_errors(LINES), [("Database timeout", 2), ("User not found", 1)], "top_errors")


def test_top_errors_n(sol):
    eq(sol.top_errors(LINES, n=1), [("Database timeout", 2)], "top_errors with n=1")
