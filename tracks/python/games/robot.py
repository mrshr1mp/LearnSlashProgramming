"""Robot Maze runner. Usage: robot.py LEVEL.json SOLUTION.py

Runs your code once on every map of the level and prints one line of JSON: each map's
robot moves (the app animates them), whether it reached the flag, gems, and any error.
"""
import contextlib
import io
import json
import sys
import traceback

DIRS = {"E": (1, 0), "S": (0, 1), "W": (-1, 0), "N": (0, -1)}
LEFT = {"E": "N", "N": "W", "W": "S", "S": "E"}
RIGHT = {v: k for k, v in LEFT.items()}
MAX_STEPS, MAX_CHECKS = 400, 20_000
COMMANDS = ["move", "turn_left", "turn_right", "collect", "front_is_clear", "on_gem", "at_goal"]


class Crash(Exception):
    """The robot can't go on (hit a wall, grabbed at nothing, ran out of battery). Not a bug in Python."""


class World:
    def __init__(self, rows):
        self.walls, self.gems = set(), set()
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch == "#":
                    self.walls.add((x, y))
                elif ch == "*":
                    self.gems.add((x, y))
                elif ch == "G":
                    self.goal = (x, y)
                elif ch in "><^v":
                    self.pos, self.dir = (x, y), {">": "E", "<": "W", "^": "N", "v": "S"}[ch]
        self.size = (max(len(r) for r in rows), len(rows))
        self.total, self.checks = len(self.gems), 0
        self.steps = []

    def log(self, action):
        self.steps.append({"x": self.pos[0], "y": self.pos[1], "dir": self.dir, "action": action})
        if len(self.steps) > MAX_STEPS:
            raise Crash("battery")

    def ahead(self):
        dx, dy = DIRS[self.dir]
        return self.pos[0] + dx, self.pos[1] + dy

    def open(self, p):
        return p not in self.walls and 0 <= p[0] < self.size[0] and 0 <= p[1] < self.size[1]

    def sense(self):
        self.checks += 1
        if self.checks > MAX_CHECKS:
            raise Crash("battery")

    # ----- the commands your code can use -----
    def move(self):
        if not self.open(self.ahead()):
            self.log("bump")
            raise Crash("wall")
        self.pos = self.ahead()
        self.log("move")

    def turn_left(self):
        self.dir = LEFT[self.dir]
        self.log("turn")

    def turn_right(self):
        self.dir = RIGHT[self.dir]
        self.log("turn")

    def collect(self):
        if self.pos not in self.gems:
            self.log("grab")
            raise Crash("nothing")
        self.gems.remove(self.pos)
        self.log("collect")

    def front_is_clear(self):
        self.sense()
        return self.open(self.ahead())

    def on_gem(self):
        self.sense()
        return self.pos in self.gems

    def at_goal(self):
        self.sense()
        return self.pos == self.goal


def your_line(tb):
    lines = [f.lineno for f in traceback.extract_tb(tb) if f.filename == "your code"]
    return lines[-1] if lines else None


def run(code, rows, banned):
    world = World(rows)
    names = {name: getattr(world, name) for name in COMMANDS if name not in banned}
    out, crash, error = io.StringIO(), None, None
    try:
        program = compile(code, "your code", "exec")
        with contextlib.redirect_stdout(out):
            exec(program, names)
    except Crash as e:
        crash = {"reason": str(e), "line": your_line(e.__traceback__)}
    except SyntaxError as e:
        error = {"type": type(e).__name__, "message": e.msg, "line": e.lineno}
    except Exception as e:
        error = {"type": type(e).__name__, "message": str(e), "line": your_line(e.__traceback__)}
    return {"steps": world.steps, "won": not crash and not error and world.pos == world.goal,
            "gems": world.total - len(world.gems), "gems_total": world.total,
            "crash": crash, "error": error, "output": out.getvalue()[-2000:]}


def main(level_path, solution_path):
    level = json.load(open(level_path, encoding="utf-8"))
    code = open(solution_path, encoding="utf-8").read()
    print(json.dumps({"maps": [run(code, rows, level.get("banned", [])) for rows in level["maps"]]}))


if __name__ == "__main__":
    main(*sys.argv[1:3])
