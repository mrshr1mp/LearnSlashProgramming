import time
from itertools import count, islice

from harness import eq


def test_countdown(sol):
    c = sol.Countdown(3)
    eq(list(c), [3, 2, 1], "list(Countdown(3))")
    eq(list(c), [3, 2, 1], "looping over the same Countdown a second time")
    eq(list(sol.Countdown(0)), [], "list(Countdown(0))")


def test_fibonacci(sol):
    eq(list(islice(sol.fibonacci(), 10)), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34], "first 10 of fibonacci()")


def test_take(sol):
    eq(sol.take(3, count(5)), [5, 6, 7], "take(3, count(5)) on an infinite stream")
    eq(sol.take(5, [1, 2]), [1, 2], "take(5, [1, 2])")


def test_primes(sol):
    eq(list(islice(sol.primes(), 10)), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29], "first 10 primes")
    start = time.perf_counter()
    eq(list(islice(sol.primes(), 3000))[-1], 27449, "the 3000th prime")
    assert time.perf_counter() - start < 5, "primes() is too slow: only test divisors up to the square root"


def test_window(sol):
    eq(list(sol.window([1, 2, 3, 4], 2)), [(1, 2), (2, 3), (3, 4)], "window([1, 2, 3, 4], 2)")
    eq(list(sol.window("abcd", 3)), [("a", "b", "c"), ("b", "c", "d")], 'window("abcd", 3)')
    eq(list(sol.window([1], 2)), [], "window([1], 2)")
    eq(list(islice(sol.window(count(), 3), 2)), [(0, 1, 2), (1, 2, 3)], "window on an infinite stream")


def test_chunked(sol):
    eq(list(sol.chunked(range(7), 3)), [[0, 1, 2], [3, 4, 5], [6]], "chunked(range(7), 3)")
    eq(list(sol.chunked([], 3)), [], "chunked([], 3)")
    eq(list(islice(sol.chunked(count(), 2), 2)), [[0, 1], [2, 3]], "chunked on an infinite stream")
