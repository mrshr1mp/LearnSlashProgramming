import tempfile
from pathlib import Path

from harness import eq, raises


def sample(sol):
    t = sol.TaskList()
    t.add("low")
    t.add("urgent", priority=3)
    t.add("mid", 2)
    t.add("urgent too", priority=3)
    return t


def test_add_returns_ids(sol):
    t = sol.TaskList()
    eq(t.add("first"), 1, "first add() returns id")
    eq(t.add("second", priority=3), 2, "second add() returns id")


def test_bad_input(sol):
    t = sol.TaskList()
    raises(ValueError, t.add, "   ")
    raises(ValueError, t.add, "")
    raises(ValueError, t.add, "x", priority=5)
    raises(ValueError, t.add, "x", priority=0)


def test_pending_order(sol):
    eq(sample(sol).pending(), ["urgent", "urgent too", "mid", "low"], "pending(): priority first, then oldest")


def test_done_and_len(sol):
    t = sample(sol)
    eq(len(t), 4, "len() with 4 unfinished tasks")
    t.done(2)
    eq(t.pending(), ["urgent too", "mid", "low"], "pending() after done(2)")
    eq(len(t), 3, "len() after finishing one")


def test_done_unknown_id(sol):
    raises(KeyError, sample(sol).done, 99)


def test_save_load(sol):
    t = sample(sol)
    t.done(1)
    path = Path(tempfile.mkdtemp()) / "tasks.json"
    t.save(path)
    loaded = sol.TaskList.load(path)
    eq(loaded.pending(), ["urgent", "urgent too", "mid"], "pending() after save + load")
    eq(loaded.add("new one"), 5, "add() after load continues the ids")
    loaded.done(3)
    eq(loaded.pending(), ["urgent", "urgent too", "new one"], "done() works on loaded tasks")
