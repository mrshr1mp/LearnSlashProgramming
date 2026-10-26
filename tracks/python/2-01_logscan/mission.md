# Mission 1: Log Detective
**FIX** · 50 xp · your file: `workspace/python/kit/logscan.py`

The server went down last night. Someone wrote a script to summarize the log, but it lies.
It runs with no errors and gives wrong answers. That's the worst kind of bug, and the most common one.

This is the first tool in your **kit**: a command-line toolbox you'll grow mission by mission.
By mission 10 you'll wire every tool into one program you can run with `python -m kit`.

## What it should do
- `parse_line(line)` turns `"2026-10-01 12:00:01 [ERROR] Database timeout\n"` into `("ERROR", "Database timeout")`. No stray spaces, no newlines.
- `count_levels(lines)` counts lines per level: `{"INFO": 2, "ERROR": 3, "WARN": 1}`
- `top_errors(lines, n=3)` gives the `n` most common ERROR messages, most common first: `[("Database timeout", 2), ("User not found", 1)]`
- Real logs have blank lines. Skip them; don't crash.

## Try it
```
python workspace/python/kit/logscan.py
```
It summarizes `workspace/python/samples/server.log`. Open the log and check its answers yourself.

When you think it's fixed, hit **Check my code**.

## Debug like a programmer
Don't stare at the code hoping to spot the bug. Run small experiments:
- `print(repr(message))`: `repr` shows hidden spaces and `\n` that plain `print` hides.
- Open a REPL (type `python` in a terminal), paste one log line into a variable, and try `.split("]")` on it. See what comes back.

<details><summary>Hint 1</summary>

There are 4 bugs: one in each function, plus the blank lines.
</details>

<details><summary>Hint 2</summary>

`parse_line`: what's at the start and end of `line.split("]")[1]`? Look up `str.strip()`.
</details>

<details><summary>Hint 3</summary>

`counts[level] = 1` doesn't count anything. And `sorted` goes smallest-first unless you pass `reverse=True`.
For blank lines: `if not line.strip(): continue`.
</details>

## Level up (not graded)
- Make `python logscan.py other.log` read whatever file you name, using `sys.argv`.
- Redo the counting with `collections.Counter`. How much shorter does it get?

## Docs worth skimming
Reading docs is how you stop needing tutorials. Get used to it now.
- String methods: https://docs.python.org/3/library/stdtypes.html#string-methods
- Sorting: https://docs.python.org/3/howto/sorting.html
