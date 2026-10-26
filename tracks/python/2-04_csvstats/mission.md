# Mission 4: Spending Report
**BUILD** · 100 xp · your file: `workspace/python/kit/csvstats.py`

`samples/sales.csv` is a spending log with columns `date,category,item,amount`.
Somebody typed it by hand, so some rows are junk. Real data is always messy.
Handling the mess *is* the job.

## What to build
- `load(path)` returns a list of dicts, one per row: `{"date": "2026-10-01", "category": "food", "item": "pizza", "amount": 12.5}`
  - `amount` must be a `float`, not a string.
  - Skip rows where amount is blank or isn't a number (like `oops`). Don't crash.
- `totals_by(rows, column)` adds up `amount` for each value of `column`, rounded to 2 decimals. For example:
  `totals_by(rows, "category")` might give `{"food": 30.85, "games": 59.99, "books": 35.0}`
- `best(rows, column)` returns the `(value, total)` with the biggest total, like `("games", 59.99)`, or `None` if there are no rows.

## Try it
Write a `__main__` block that prints a little report for `samples/sales.csv`:
which category ate the most money? Which day?

Then hit **Check my code**.

<details><summary>Hint 1: reading CSV</summary>

Don't split on commas yourself (an item like `"cable, 2m"` breaks that).
`csv.DictReader` gives you each row as a dict already.
</details>

<details><summary>Hint 2: bad numbers</summary>

`float("oops")` raises `ValueError`. Catch it with `try/except ValueError` and `continue`.
`float("")` raises the same error, so one `except` covers both.
</details>

<details><summary>Hint 3: best</summary>

`max(some_dict.items(), key=...)`. Same `key=` idea as sorting in mission 2.
</details>

## Level up (not graded)
- Print a text bar chart: `food  ######## 30.85`
- Add `--month 2026-10` that only counts rows from that month.

## Docs
- csv: https://docs.python.org/3/library/csv.html
- Errors and exceptions: https://docs.python.org/3/tutorial/errors.html
