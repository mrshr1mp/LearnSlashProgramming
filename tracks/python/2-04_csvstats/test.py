import tempfile
from pathlib import Path

from harness import eq

CSV = """date,category,item,amount
2026-10-01,food,pizza,12.50
2026-10-01,games,controller,59.99
2026-10-02,food,tacos,8.25
2026-10-03,books,"python book, used",35
2026-10-03,food,coffee,
2026-10-04,games,skin,oops
2026-10-05,food,burger,10.10
"""


def rows(sol):
    path = Path(tempfile.mkdtemp()) / "sales.csv"
    path.write_text(CSV)
    return sol.load(path)


def test_load(sol):
    got = rows(sol)
    eq(len(got), 5, "number of rows (blank and 'oops' amounts are skipped)")
    eq(got[0], {"date": "2026-10-01", "category": "food", "item": "pizza", "amount": 12.5}, "first row")
    eq(got[3]["item"], "python book, used", "item with a comma inside quotes")
    assert all(isinstance(r["amount"], float) for r in got), "every amount should be a float"


def test_totals_by(sol):
    data = rows(sol)
    eq(sol.totals_by(data, "category"), {"food": 30.85, "games": 59.99, "books": 35.0}, 'totals_by(rows, "category")')
    eq(sol.totals_by(data, "date"), {"2026-10-01": 72.49, "2026-10-02": 8.25, "2026-10-03": 35.0, "2026-10-05": 10.1},
       'totals_by(rows, "date")')


def test_best(sol):
    data = rows(sol)
    eq(sol.best(data, "category"), ("games", 59.99), 'best(rows, "category")')
    eq(sol.best(data, "date"), ("2026-10-01", 72.49), 'best(rows, "date")')
    eq(sol.best([], "category"), None, "best([], ...)")
