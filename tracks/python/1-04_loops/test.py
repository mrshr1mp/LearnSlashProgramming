from harness import eq


def test_sum_to(sol):
    eq(sol.sum_to(4), 10, "sum_to(4)")
    eq(sol.sum_to(100), 5050, "sum_to(100)")
    eq(sol.sum_to(0), 0, "sum_to(0)")


def test_count_vowels(sol):
    eq(sol.count_vowels("Programming"), 3, 'count_vowels("Programming")')
    eq(sol.count_vowels("AEIOU and sometimes y"), 10, 'count_vowels("AEIOU and sometimes y")')
    eq(sol.count_vowels("rhythm"), 0, 'count_vowels("rhythm")')


def test_reverse(sol):
    eq(sol.reverse("loop"), "pool", 'reverse("loop")')
    eq(sol.reverse("Hello!"), "!olleH", 'reverse("Hello!")')
    eq(sol.reverse(""), "", 'reverse("")')


def test_stars(sol):
    eq(sol.stars(3), "*\n**\n***", "stars(3)")
    eq(sol.stars(1), "*", "stars(1)")


def test_collatz_steps(sol):
    eq(sol.collatz_steps(6), 8, "collatz_steps(6)")
    eq(sol.collatz_steps(1), 0, "collatz_steps(1)")
    eq(sol.collatz_steps(27), 111, "collatz_steps(27)")
