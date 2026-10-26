# Mission 10: BOSS: The Kit
**BOSS** · 250 xp · your file: `workspace/python/kit/__main__.py` (it starts empty)

You've built a pile of separate tools. Now turn them into **one real program**, the way
`git`, `pip` and `python` itself work: one command, many subcommands.

```
cd workspace/python
python -m kit --help
python -m kit logscan samples/server.log
python -m kit words samples/zen.txt --top 5
python -m kit organize samples/messy
python -m kit organize samples/messy --go
python -m kit dupes samples/backup
```
`python -m kit` runs `kit/__main__.py`. Inside it you can `from kit import logscan, wordfreq, organize, dupes`.

**No starter code. No skeleton. A blank file.** This is the tutorial-hell exit exam.
Everything you need, you've used before or it's in the docs linked below.

## Exact output the tests expect
| command | prints |
|---|---|
| `logscan FILE` | one line per level, `LEVEL: count`, highest count first (ties alphabetical) |
| `words FILE [--top N]` | one line per word, `word count`, top 10 unless `--top` says otherwise |
| `organize FOLDER` | one line per file, `name -> folder`, sorted by name. Moves nothing. |
| `organize FOLDER --go` | same lines, actually moves the files, then a last line `moved N files` |
| `dupes FOLDER` | each group's paths one per line, a blank line between groups, or `no duplicates` |
| `--help` | a usage message that lists the commands; exit code 0 |
| an unknown command | an error message; exit code not 0 |

Then hit **Check my code** (it runs your earlier tools too, so they need to still work).

## How to start on a blank file
Real programmers get stuck too. Here's what they do:
1. Get *anything* running. `print("hello from kit")`, then run `python -m kit`. Good.
2. Make **one** command work, the easiest one, all the way through. Run it.
3. Add the next one. Run it again.
4. Never write 100 lines and then run it for the first time.

<details><summary>Hint 1: which module?</summary>

`argparse`, from the standard library. You've been *using* it this whole time: `learn.py` is built on it. Go read `learn.py`'s `main()`.
</details>

<details><summary>Hint 2: subcommands</summary>

Search the argparse docs for `add_subparsers`. Each subcommand gets its own parser with its own arguments.
Use `dest="command"` so you can tell which one was picked.
</details>

<details><summary>Hint 3: --go</summary>

`add_argument("--go", action="store_true")` gives you `True` if the flag is there and `False` if not.
</details>

## You beat the boss. Now what?
- Add your mission 5 and 8 tools as commands too: `python -m kit decode FILE`, `python -m kit islands FILE`.
- Add tasks from mission 6: `python -m kit todo add "..."`. Your kit is now a real app you use.
- Go do Advent of Code (adventofcode.com). Past years are all still up.
- Build something nobody assigned you. That's the real final level.

## Docs
- argparse tutorial: https://docs.python.org/3/howto/argparse.html
- argparse subcommands: https://docs.python.org/3/library/argparse.html#sub-commands
