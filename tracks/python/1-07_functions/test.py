from harness import eq


def double(n):
    return n * 2


def test_clamp(sol):
    eq(sol.clamp(150), 100, "clamp(150)")
    eq(sol.clamp(-5), 0, "clamp(-5)")
    eq(sol.clamp(42), 42, "clamp(42)")
    eq(sol.clamp(7, low=10, high=20), 10, "clamp(7, low=10, high=20)")
    eq(sol.clamp(30, high=25), 25, "clamp(30, high=25)")


def test_make_greeting(sol):
    eq(sol.make_greeting("Ada"), "Hello, Ada!", 'make_greeting("Ada")')
    eq(sol.make_greeting("Ada", punctuation="?"), "Hello, Ada?", 'make_greeting("Ada", punctuation="?")')
    eq(sol.make_greeting("Bob", "Yo"), "Yo, Bob!", 'make_greeting("Bob", "Yo")')


def test_stats(sol):
    eq(sol.stats([4, 1, 7]), (1, 7, 4.0), "stats([4, 1, 7])")
    eq(sol.stats([1, 2]), (1, 2, 1.5), "stats([1, 2])")
    eq(sol.stats([1, 1, 2]), (1, 2, 1.33), "stats([1, 1, 2])")
    eq(sol.stats([]), (None, None, None), "stats([])")


def test_apply_n(sol):
    eq(sol.apply_n(double, 3, 2), 12, "apply_n(double, 3, 2)")
    eq(sol.apply_n(double, 1, 10), 1024, "apply_n(double, 1, 10)")
    eq(sol.apply_n(str.upper, "hi", 1), "HI", 'apply_n(str.upper, "hi", 1)')
    eq(sol.apply_n(double, 5, 0), 5, "apply_n(double, 5, 0)")


def test_best_by(sol):
    eq(sol.best_by(["kiwi", "banana", "fig"], len), "banana", 'best_by(["kiwi", "banana", "fig"], len)')
    eq(sol.best_by(["ab", "cd", "e"], len), "ab", 'best_by(["ab", "cd", "e"], len) (tie goes to the first)')
    eq(sol.best_by([3, -9, 4], abs), -9, "best_by([3, -9, 4], abs)")
    eq(sol.best_by([], len), None, "best_by([], len)")
