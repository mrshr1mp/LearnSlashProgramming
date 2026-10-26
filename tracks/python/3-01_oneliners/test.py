import ast
from pathlib import Path

from harness import eq

NAMES = ["squares_of_evens", "word_lengths", "first_letters", "numbered", "all_positive", "has_duplicates",
         "transpose", "flatten", "total_price"]


def test_answers_still_right(sol):
    eq(sol.squares_of_evens([1, 2, 3, 4]), [4, 16], "squares_of_evens([1, 2, 3, 4])")
    eq(sol.word_lengths(["hi", "hey"]), {"hi": 2, "hey": 3}, 'word_lengths(["hi", "hey"])')
    eq(sol.first_letters(["ada", "Alan", "", "bob"]), {"A", "B"}, 'first_letters(["ada", "Alan", "", "bob"])')
    eq(sol.numbered(["apple", "pear"]), ["1. apple", "2. pear"], 'numbered(["apple", "pear"])')
    eq(sol.all_positive([1, 2, 3]), True, "all_positive([1, 2, 3])")
    eq(sol.all_positive([1, 0, 3]), False, "all_positive([1, 0, 3])")
    eq(sol.all_positive([]), True, "all_positive([])")
    eq(sol.has_duplicates([1, 2, 1]), True, "has_duplicates([1, 2, 1])")
    eq(sol.has_duplicates("abc"), False, 'has_duplicates("abc")')
    eq(sol.transpose([[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]], "transpose([[1, 2, 3], [4, 5, 6]])")
    eq(sol.transpose([]), [], "transpose([])")
    eq(sol.flatten([[1, 2], [], [3]]), [1, 2, 3], "flatten([[1, 2], [], [3]])")
    eq(sol.total_price([{"price": 2.5, "qty": 4}, {"price": 1, "qty": 3}]), 13.0, "total_price(...)")


def single_return(fn):
    body = fn.body[1:] if fn.body and isinstance(fn.body[0], ast.Expr) and isinstance(fn.body[0].value, ast.Constant) else fn.body
    return len(body) == 1 and isinstance(body[0], ast.Return)


def check_one_liner(name):
    def test(sol):
        tree = ast.parse(Path(sol.__file__).read_text(encoding="utf-8"))
        fns = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
        assert name in fns, f"couldn't find the function {name}"
        assert single_return(fns[name]), f"{name} should be a single `return ...` line (it has {len(fns[name].body)} statements)"
    return test


for _name in NAMES:
    globals()[f"test_{_name}_is_one_line"] = check_one_liner(_name)
