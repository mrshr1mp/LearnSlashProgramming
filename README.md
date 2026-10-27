# LearnProgramming

Learn a language by building real tools, not by answering quizzes.

**Double-click `Start Learning.bat`** (or run `python app.py`; on Linux/macOS run `./start.sh`). The app opens in its own window:
read the mission, hit **Start mission** (opens your file in VS Code), write code, save, then hit
**Check my code** or press **Ctrl+Enter**. No console window: the app closes itself a few minutes after you close its window. If something goes wrong, `workspace/app.log` has the details.

Prefer the terminal? Same thing without the app:
```
python learn.py            # your missions, XP and rank
python learn.py start 1    # sets up mission 1 and opens it in VS Code
python learn.py check 1    # runs the tests on your code
```

## Learning with friends
The app asks you to sign in (or **Register**) when it opens. Add friends by username, and once they accept you can
see each other's progress, activity and achievements on the **Friends** page. You can also read a friend's code for
any mission **you've already finished yourself**, side by side with yours. Set a profile picture on the **Account** page.

Each computer's progress belongs to the first account that signs in on it, so one person's missions can't
end up on someone else's account. Everyone uses their own copy of the app.

**Setting it up on a new computer** (for a friend):
1. Install [Python](https://www.python.org/downloads/) (tick "Add python.exe to PATH") and [VS Code](https://code.visualstudio.com/).
2. Get the code: `git clone <repo link>`, then open the folder.
3. Double-click `Start Learning.bat` and **Register**.

**On Linux** (commands for Ubuntu/Debian; other distros use their own package manager):
1. `sudo apt install python3 git`, plus [VS Code](https://code.visualstudio.com/) (its `code` command lets the app open your files).
   For the app's own window, have Chrome, Chromium, Edge or Brave installed; with only Firefox it opens as a normal tab.
2. `git clone <repo link>`, then `cd` into the folder.
3. Run `./start.sh` and **Register**. You can close the terminal after that.
4. Everywhere the lessons say `python`, type `python3`.

**One-click updates.** The app opens right away and checks GitHub in the background. If there's a new version, an
**Update available** banner appears within a few seconds (and it keeps checking every 10 minutes while open).
Click **Update now** and it downloads, restarts and reloads by itself.
Updates never touch `workspace/`, so nobody's code or progress is affected.

**Shipping an update** (for whoever maintains the app): commit, then `git push`. Write a clear first line in the
commit message; that's what everyone sees in the banner. Database changes (`supabase/schema.sql`) reach
everyone instantly, so keep them compatible with older copies of the app that haven't updated yet.

**What's private:** your code and progress live on your computer in `workspace/`, which git never uploads.
Signing in syncs a copy to the shared database, where only friends you've accepted can read it
(the rules are in `supabase/schema.sql` and are enforced by the database itself). `cloud.json` only holds the
*publishable* key, which is designed to be public. Your login session stays in `workspace/session.json`.

## Marketplace
Nobody starts with any courses. Open **Marketplace** in the app and click **Add course** to download one into
`workspace/courses/`. When a course gets new missions you'll see **Update** there; your code and progress are
kept when you update or remove a course. (If you used the app before the marketplace existed, the courses you'd
already started were added for you.)

Publishing (only accounts listed as publishers in the database can do this): sign in to the app, then run
`python tools/publish_course.py <course id>` to upload `tracks/<course id>/`. Every publish bumps the version.

## Games
The **Games** tab has real games for each course you've added. Every game gives XP, and friends see your scores.
- **Robot Maze:** 12 levels. Write real code to steer a robot to the flag; loops, ifs and functions unlock harder mazes.
  Three stars per level: reach the flag, grab every gem, use par lines or fewer.
- **Bug Invaders:** lines of code fall from the sky. Shoot the buggy ones, let the good ones land.
- **Code Racer:** type real code as fast as you can, racing your best time (and your fastest friend).

**Play with friends:** in Games, click **Create a game** and send your friends the 6-letter code; they type it
into **Join**. The first player in the room is the host and picks **Code Race**, **Bug Blitz** or **Robot Race**.
Everyone plays on their own screen with a live scoreboard, and the winner gets the most XP. Rooms run on Supabase
Realtime; only signed-in players can join (the rules are at the end of `supabase/schema.sql`).

A course's games live in `tracks/<course>/games/`: `robot.json` (levels: `maps` drawn with `#` walls, `*` gems,
`G` flag and `>` `<` `^` `v` for the robot), `robot.py` (runs the robot; `track.json` says how under `"robot"`),
`invaders.json` (lines with `"ok": true` or a `"bug"` explanation) and `racer.txt` (snippets split by `---`).

## How it works
Every mission gives you a brief (`mission.md`) and a file to work in (`workspace/python/kit/...`).
You write real code in a real editor. `check` runs hidden tests against it and tells you exactly what's wrong.
There are no multiple-choice questions. The only way to pass is to make the code work.

There are 27 missions in three chapters, from zero to "I know Python":

| chapter | missions | what it covers |
|---|---|---|
| **Foundations** | 8 | each one starts with a short lesson: strings, numbers, if/else, loops, lists, dicts, functions. The boss is a text adventure engine you can play. |
| **The Kit** | 10 | real tools that grow into one project, `kit`, your own command-line toolbox: files, CSV, classes, recursion, algorithms. The boss wires it all into `python -m kit`. |
| **Deep Python** | 9 | comprehensions, decorators, generators, dunder methods, exceptions and context managers, dataclasses, regex, writing your own tests. The final boss is a programming language interpreter. |

The help gets smaller as you go:

| kind | what you get |
|---|---|
| LEARN | a lesson, then a mission with outlines to fill in |
| FIX | working-looking code that's secretly broken |
| FILL | function outlines with TODO steps |
| BUILD | just the function names and a spec |
| PUZZLE | a problem where figuring out *how* is the hard part |
| REFACTOR | working code you have to rewrite better |
| TESTS | you write the tests, and they have to catch hidden bugs |
| BOSS | a blank file (or close to it) |

## Rules (for yourself)
1. Try for 10 minutes before opening a hint. Being stuck is where the learning happens.
2. The Python docs are always allowed. Reading docs is the skill that gets you out of tutorial hell.
3. Run your code constantly. Use the REPL (`python` in a terminal) to test one small thing at a time.
4. Do at least one "Level up" from each mission. Those are where you go from "knows basic Python" to "knows Python".
5. You *can* read `test.py` if you're confused about what's expected. Reading tests is a real-world skill too.

## Folders
```
Start Learning.bat       double-click to launch the app (Windows)
start.sh                 ./start.sh to launch the app (Linux/macOS)
app.py                   the app's local server (only reachable from your own PC)
cloud.py, cloud.json     accounts, syncing and friends (Supabase)
supabase/schema.sql      the database tables and privacy rules
ui.html                  the app's screen
learn.py                 mission control (start, check, progress), also usable on its own
tools/publish_course.py  uploads a course to the marketplace (publishers only)
tracks/python/           the Python course's source (what gets published)
  track.json             how to run tests, rank names, plain-English error explanations
  harness.py             the test runner
  01_logscan/            one mission: mission.md, starter.py, test.py, samples/
workspace/               YOUR code, progress and added courses (never uploaded to git)
```

## Adding more
**A new mission:** make a folder in `tracks/python/` like `3-10_something/` (chapter number, then order) with:
- `mission.json`: `{"chapter": "Deep Python", "title": "...", "kind": "BUILD", "xp": 150, "file": "deep/something.py"}`
- `mission.md`: the brief
- `test.py`: functions named `test_*(sol)` where `sol` is the learner's module. Use `eq` and `raises` from `harness`.
- optional `starter.py` and a `samples/` folder

The folder name sets the order. You can ask Claude to write a "season 2" of missions in this format.
Publish the course again afterwards so everyone gets the new missions.

**A new language:** make `tracks/<language>/` with its own `track.json`, harness and missions.
The `run` command in `track.json` says how to test a solution, e.g. `["node", "{track}/harness.js", "{test}", "{solution}"]`.
The harness must print one line per test: `  PASS   name`, `  FAIL   name: message`, `  CRASH  name: ...` or `  TODO   name: ...`
(that's what the app reads). A language picker shows up in the app once there's more than one track.
