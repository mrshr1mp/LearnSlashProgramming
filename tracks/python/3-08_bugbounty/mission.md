# Mission 8: Bug Bounty
**TESTS** · 225 xp · your file: `workspace/python/deep/test_textkit.py`

All along, hidden tests have checked *your* code. Now the roles flip: **you write the tests.**

Writing good tests is what separates hobby code from professional code. It's also the fastest way to find out
whether you really understand what a function should do, including the weird edge cases.

## How this mission is graded
`samples/textkit.py` contains three working functions (spec below). The grader has **8 secret broken versions** of textkit,
each with a different, realistic bug. Your tests are run against:
1. the **real** textkit: every one of your tests must pass, and
2. each **broken** version: at least one of your tests must fail. That's a bug caught!

The more edge cases you think of, the more bugs you catch. Catch all 8 to win.

## The functions under test
**`slugify(title)`** turns a title into a URL-friendly slug:
lowercase, every run of non-letter/non-digit characters becomes a **single** `-`, and no `-` at the start or end.
```python
slugify("Hello, World!")              # "hello-world"
slugify("  Python   3.13 rocks ")     # "python-3-13-rocks"
```

**`clamp(x, low, high)`** limits x to the range low..high.
```python
clamp(5, 0, 10)    # 5
clamp(-3, 0, 10)   # 0
clamp(99, 0, 10)   # 10
```

**`parse_duration(text)`** turns `"1h30m"`-style text into seconds. Each of h, m, s is optional, but they always come in that order.
```python
parse_duration("1h30m")    # 5400
parse_duration("45s")      # 45
parse_duration("1h2m3s")   # 3723
parse_duration("")         # raises ValueError
parse_duration("abc")      # raises ValueError
```

## How to write a test here
Each test is a function whose name starts with `test_`. It takes `m`, the module being tested, and uses `assert`:
```python
def test_slugify_simple(m):
    assert m.slugify("Hello World") == "hello-world"
```
Checking that something raises an error:
```python
def test_empty_duration_fails(m):
    try:
        m.parse_duration("")
    except ValueError:
        return                 # good, it raised
    assert False, "should have raised ValueError"
```
Run your file directly (▶) to try your tests against the real textkit before you check.

<details><summary>Hint: what kinds of bugs?</summary>

Think about what a hurried programmer might get wrong: forgetting to lowercase, not trimming the ends,
not collapsing repeated symbols, mixing up the boundaries in clamp, dropping one of the h/m/s parts, or not raising on bad input.
</details>

<details><summary>Hint: edge cases</summary>

The best tests sit right on the boundaries: x exactly at `low` or `high`, the smallest and biggest inputs, empty strings, and inputs with only the "weird" parts.
</details>

## Level up (not graded)
- Install **pytest** (`pip install pytest`). It's the real-world tool for this, and it uses plain `assert` too.
- Look up "property-based testing" and the `hypothesis` library. It generates thousands of test inputs for you.
