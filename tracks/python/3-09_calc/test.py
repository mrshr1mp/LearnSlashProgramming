import re
from pathlib import Path

from harness import eq


def calc(sol):
    assert hasattr(sol, "Calculator"), "define a class called Calculator"
    return sol.Calculator()


def expect_error(sol, c, text):
    assert hasattr(sol, "CalcError"), "define class CalcError(Exception)"
    try:
        c.run(text)
    except sol.CalcError:
        return
    except Exception as e:
        raise AssertionError(f"run({text!r}) raised {type(e).__name__}: {e}. It should raise CalcError instead")
    raise AssertionError(f"run({text!r}) should raise CalcError, but it didn't")


def test_no_eval(sol):
    source = Path(sol.__file__).read_text(encoding="utf-8")
    assert not re.search(r"\b(eval|exec)\s*\(", source), "eval() and exec() are banned. Build the parser yourself!"


def test_numbers(sol):
    c = calc(sol)
    eq(c.run("42"), 42, 'run("42")')
    eq(c.run("1.5 * 2"), 3.0, 'run("1.5 * 2")')
    eq(c.run("  7  "), 7, 'run("  7  ")')


def test_precedence(sol):
    c = calc(sol)
    for text, want in [("2 + 3 * 4", 14), ("(2 + 3) * 4", 20), ("2*(3+4)", 14), ("10 / 4", 2.5),
                       ("2 * 3 + 4 * 5", 26), ("((1))", 1)]:
        eq(c.run(text), want, f"run({text!r})")


def test_left_to_right(sol):
    c = calc(sol)
    eq(c.run("8 - 3 - 2"), 3, 'run("8 - 3 - 2")')
    eq(c.run("16 / 4 / 2"), 2, 'run("16 / 4 / 2")')


def test_power(sol):
    c = calc(sol)
    eq(c.run("2 ^ 10"), 1024, 'run("2 ^ 10")')
    eq(c.run("2 ^ 3 ^ 2"), 512, 'run("2 ^ 3 ^ 2") (right to left)')
    eq(c.run("2 * 3 ^ 2"), 18, 'run("2 * 3 ^ 2")')


def test_unary_minus(sol):
    c = calc(sol)
    for text, want in [("-3 + 5", 2), ("2 * -(1 + 2)", -6), ("--4", 4), ("-2 ^ 2", -4)]:
        eq(c.run(text), want, f"run({text!r})")


def test_variables(sol):
    c = calc(sol)
    eq(c.run("let x = 5"), 5, 'run("let x = 5")')
    eq(c.run("let y = x * 2 + 1"), 11, 'run("let y = x * 2 + 1")')
    eq(c.run("x + y"), 16, 'run("x + y")')
    eq(c.run("let my_var = (x - 1) ^ 2"), 16, 'run("let my_var = (x - 1) ^ 2")')
    eq(c.run("let x = x + 1"), 6, 'run("let x = x + 1")')
    eq(calc(sol).run("let x = 1") + c.run("x"), 7, "two Calculators keep separate variables")


def test_errors(sol):
    c = calc(sol)
    for text in ["z + 1", "1 / 0", "2 +", "(1 + 2", "1 + 2)", "2 3", "3 $ 4", "", "let = 5", "let 5 = x", "* 3"]:
        expect_error(sol, c, text)
    eq(c.run("1 + 1"), 2, "the calculator still works after errors")
