# Mission 1: One-Liners
**REFACTOR** · 150 xp · your file: `workspace/python/deep/oneliners.py`

Welcome to Deep Python. This chapter is the difference between "I know some Python" and "I know Python".

Every function in your file **already works**. It's also long-winded, loop-and-append code.
Your job: rewrite each one so its body is a **single `return` line**. The tests check both things:
the answers are still right, *and* each function is one line.

This is called **refactoring**: changing how code is written without changing what it does. It's a huge part of real programming.

## Lesson: comprehensions
A list comprehension is a loop-and-append, squeezed into one expression:
```python
# long way
result = []
for n in nums:
    if n > 0:
        result.append(n * 10)

# comprehension: [what_to_keep  for item in things  if condition]
result = [n * 10 for n in nums if n > 0]
```
Dicts and sets get them too:
```python
{w: len(w) for w in words}         # dict comprehension
{w[0] for w in words}              # set comprehension (no duplicates)
```
You can nest them. The `for`s read left to right, in the same order as nested loops:
```python
[cell for row in grid for cell in row]    # flatten a 2D grid
```

## Lesson: generator expressions
Drop the brackets inside a function call, and you get a lazy stream that doesn't build a list in memory:
```python
sum(n * n for n in range(1_000_000))
any(n < 0 for n in nums)      # True if at least one is negative (stops early!)
all(n > 0 for n in nums)      # True if every one is positive
```

## Lesson: zip and enumerate
```python
for name, score in zip(names, scores):     # walk two lists side by side
    ...
for i, name in enumerate(names, start=1):  # get a counter for free
    ...
list(zip([1, 2], ["a", "b"]))              # [(1, 'a'), (2, 'b')]
list(zip(*[[1, 2], [3, 4]]))               # [(1, 3), (2, 4)]: the * "unpacks" the rows. This transposes!
```

## Lesson: conditional expression
```python
label = "even" if n % 2 == 0 else "odd"
```

## Your mission
Rewrite all 9 functions in `oneliners.py`. Each body must be exactly one `return` statement.
(A docstring on top is allowed.)

**When *not* to use one-liners:** if a comprehension needs three `if`s and two nested `for`s, a normal loop is easier to read.
Readable beats clever. These 9 are all good fits, though.

<details><summary>Hint: numbered</summary>

`[f"{i}. {item}" for i, item in enumerate(items, start=1)]`
</details>

<details><summary>Hint: transpose</summary>

`zip(*matrix)` gives tuples. The tests want lists, so wrap each one in `list(...)`, inside a comprehension.
</details>

<details><summary>Hint: total_price</summary>

`sum(...)` of a generator expression over the cart.
</details>

## Level up (not graded)
- `python -m timeit` lets you time code. Compare the loop version of `squares_of_evens` with the comprehension version on a big list.
- Look up `itertools` and `functools.reduce`. Which functions in the standard library could replace the loops you wrote in Chapter 1?
