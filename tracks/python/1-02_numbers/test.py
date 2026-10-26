from harness import eq


def test_average(sol):
    eq(sol.average(1, 2, 4), 7 / 3, "average(1, 2, 4)")
    eq(sol.average(10, 10, 10), 10, "average(10, 10, 10)")


def test_tip(sol):
    eq(sol.tip(23.80, 18), 4.28, "tip(23.80, 18)")
    eq(sol.tip(50, 20), 10.0, "tip(50, 20)")


def test_celsius(sol):
    eq(sol.celsius(212), 100.0, "celsius(212)")
    eq(sol.celsius(98.6), 37.0, "celsius(98.6)")
    eq(sol.celsius(0), -17.8, "celsius(0)")


def test_clock(sol):
    eq(sol.clock(3725), "1:02:05", "clock(3725)")
    eq(sol.clock(59), "0:00:59", "clock(59)")
    eq(sol.clock(36000), "10:00:00", "clock(36000)")


def test_is_even(sol):
    eq(sol.is_even(10), True, "is_even(10)")
    eq(sol.is_even(7), False, "is_even(7)")
    eq(sol.is_even(0), True, "is_even(0)")
