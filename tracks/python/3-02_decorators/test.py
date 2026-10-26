import time

from harness import eq, raises


def test_make_counter(sol):
    a, b = sol.make_counter(), sol.make_counter()
    eq([a(), a(), a()], [1, 2, 3], "three calls to one counter")
    eq(b(), 1, "first call to a second, separate counter")
    eq(a(), 4, "the first counter keeps going")


def test_count_calls(sol):
    @sol.count_calls
    def add(x, y=0):
        """adds"""
        return x + y

    eq(add.calls, 0, ".calls before any call")
    eq(add(2, y=3), 5, "add(2, y=3) through the decorator")
    add(1)
    eq(add.calls, 2, ".calls after two calls")
    eq(add.__name__, "add", "__name__ of the decorated function (use functools.wraps)")


def test_memoize(sol):
    runs = []

    @sol.memoize
    def slow_square(n):
        runs.append(n)
        return n * n

    eq([slow_square(4), slow_square(4), slow_square(5)], [16, 16, 25], "results")
    eq(runs, [4, 5], "times the real function ran (the second slow_square(4) should come from the cache)")


def test_memoize_fib(sol):
    @sol.memoize
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    start = time.perf_counter()
    eq(fib(80), 23416728348467685, "fib(80)")
    assert time.perf_counter() - start < 1, "fib(80) took too long: is the cache being used for the recursive calls?"


def test_retry_succeeds(sol):
    attempts = []

    @sol.retry(3)
    def flaky():
        attempts.append(1)
        if len(attempts) < 3:
            raise ConnectionError("network hiccup")
        return "ok"

    eq(flaky(), "ok", "flaky() with retry(3) (it fails twice, then works)")
    eq(len(attempts), 3, "number of attempts")


def test_retry_gives_up(sol):
    attempts = []

    @sol.retry(2)
    def broken(x):
        attempts.append(x)
        raise ValueError(f"bad {len(attempts)}")

    raises(ValueError, broken, 7)
    eq(attempts, [7, 7], "attempts made by retry(2) (it should pass the arguments through)")
