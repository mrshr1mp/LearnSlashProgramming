from harness import eq


def test_grade(sol):
    for score, want in [(95, "A"), (90, "A"), (89, "B"), (80, "B"), (75, "C"), (60, "D"), (59, "F"), (0, "F"), (100, "A")]:
        eq(sol.grade(score), want, f"grade({score})")


def test_grade_invalid(sol):
    eq(sol.grade(101), "invalid", "grade(101)")
    eq(sol.grade(-5), "invalid", "grade(-5)")


def test_fizzbuzz(sol):
    for n, want in [(3, "Fizz"), (5, "Buzz"), (15, "FizzBuzz"), (30, "FizzBuzz"), (7, "7"), (9, "Fizz"), (1, "1")]:
        eq(sol.fizzbuzz(n), want, f"fizzbuzz({n})")


def test_password_strength(sol):
    cases = [("abc12", "weak"), ("abcdefghijkl", "weak"), ("123456789012", "weak"),
             ("hunter2go", "ok"), ("correct-horse", "strong"), ("Tr0ub4dor&3x", "strong"), ("pass word", "ok")]
    for pw, want in cases:
        eq(sol.password_strength(pw), want, f"password_strength({pw!r})")


def test_ticket_price(sol):
    cases = [((3, False), 0), ((3, True), 0), ((70, True), 6), ((65, False), 6), ((12, False), 8),
             ((30, True), 8), ((30, False), 12), ((18, False), 12)]
    for (age, student), want in cases:
        eq(sol.ticket_price(age, student), want, f"ticket_price({age}, {student})")
