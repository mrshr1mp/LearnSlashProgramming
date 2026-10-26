# Mission 7: Function Forge
**LEARN** · 55 xp · your file: `workspace/python/basics/functions.py`

You've been writing functions since mission 1. Now learn the tricks that make them flexible.

## Lesson: default values
Give a parameter a default, and callers can leave it out:
```python
def power(base, exp=2):
    return base ** exp

power(5)       # 25 (exp is 2 by default)
power(5, 3)    # 125
```

## Lesson: keyword arguments
You can name arguments when you call a function. Then the order doesn't matter, and the call is easier to read:
```python
def make_tag(text, tag="p", cls=""):
    ...

make_tag("hi", cls="big")      # skip tag, set cls by name
```

## Lesson: returning more than one thing
Return several values separated by commas. That makes a **tuple**, which you can unpack into separate variables:
```python
def min_max(nums):
    return min(nums), max(nums)

low, high = min_max([3, 9, 1])    # low = 1, high = 9
```

## Lesson: None
A function without a `return` gives back `None`, which is Python's "nothing".
You can also return `None` on purpose, to say "there's no answer here".
```python
def first_even(nums):
    for n in nums:
        if n % 2 == 0:
            return n      # return exits the function immediately, even mid-loop
    return None           # we got through the whole list without finding one
```

## Lesson: functions are values
A function is a thing, like a number or a string. You can store it in a variable and pass it to another function:
```python
def double(n):
    return n * 2

f = double          # no () : we're not calling it, we're passing it around
f(10)               # 20

def apply_twice(func, x):
    return func(func(x))

apply_twice(double, 3)    # double(double(3)) = 12
```
`sorted`, `max` and `min` use this too: `max(words, key=len)` gives back the longest word.
Here `len` is passed **in** as a function.

## Lesson: scope
Variables made inside a function only exist inside that function. That's a good thing: functions can't trample each other's variables.

## Your mission
| function | example | returns |
|---|---|---|
| `clamp(x, low=0, high=100)` | `clamp(150)` | `100`. Keep x between low and high |
| `make_greeting(name, greeting="Hello", punctuation="!")` | `make_greeting("Ada", punctuation="?")` | `"Hello, Ada?"` |
| `stats(numbers)` | `stats([4, 1, 7])` | `(1, 7, 4.0)` (min, max, average rounded to 2 decimals) |
| `apply_n(func, value, n)` | `apply_n(double, 3, 2)` | `12`: call func on value, n times over |
| `best_by(items, score)` | `best_by(["kiwi", "banana", "fig"], len)` | `"banana"`: the item with the highest `score(item)` |

- `stats([])` returns `(None, None, None)`.
- `best_by` returns the **first** item if there's a tie, and `None` for an empty list. Write it with a loop, not `max`. That's the point!

<details><summary>Hint: apply_n</summary>

A `for` loop that runs n times, doing `value = func(value)` each time.
</details>

<details><summary>Hint: best_by</summary>

Keep track of `best_item` and `best_score` as you loop. Only replace them when you find a **strictly** bigger score (`>`, not `>=`). That's what makes ties go to the first item.
</details>

## Level up (not graded)
- Look up `lambda`. Then `best_by(words, lambda w: w.count("a"))` finds the word with the most a's, with no separate function needed.
- Look up `*args`. Write `average(*nums)` so `average(1, 2, 3, 4)` works with any number of arguments.
