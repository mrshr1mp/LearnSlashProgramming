# Mission 2: Number Crunch
**LEARN** · 30 xp · your file: `workspace/python/basics/numbers.py`

Computers are very fast calculators, so let's make Python do math.

## Lesson: two kinds of numbers
- **int**: whole numbers like `7`, `-3`, `1000000`
- **float**: numbers with a decimal point like `3.14`, `0.5`, `2.0`

```python
>>> type(7)
<class 'int'>
>>> type(7.0)
<class 'float'>
```

## Lesson: the math operators
| operator | does | example | result |
|---|---|---|---|
| `+` `-` `*` | add, subtract, multiply | `6 * 7` | `42` |
| `/` | divide (always gives a float) | `7 / 2` | `3.5` |
| `//` | divide and drop the remainder | `7 // 2` | `3` |
| `%` | remainder ("modulo") | `7 % 2` | `1` |
| `**` | power | `2 ** 10` | `1024` |

`//` and `%` are a team. They split something into "how many whole ones" and "what's left over":
```python
total_minutes = 135
hours = total_minutes // 60     # 2
minutes = total_minutes % 60    # 15
```
`%` is also how you check if a number is even: `n % 2 == 0` means "dividing by 2 leaves nothing over".

## Lesson: rounding and converting
```python
round(3.14159, 2)    # 3.14
round(2.5)           # 2 (Python rounds .5 to the nearest even number. Weird, but true)
int("42")            # 42    (text to number)
float("3.5")         # 3.5
str(42)              # "42"  (number to text)
int(3.99)            # 3     (chops off the decimal, doesn't round)
```

## Lesson: formatting numbers in f-strings
After the variable inside `{}`, a colon adds formatting:
```python
n = 5
f"{n:02}"         # '05'    (at least 2 digits, padded with zeros)
price = 3.5
f"{price:.2f}"    # '3.50'  (exactly 2 decimal places)
```

## Lesson: True and False
A comparison gives back a **boolean**: `True` or `False`.
```python
5 > 3        # True
5 == 3       # False   (== compares, = assigns. Don't mix them up!)
5 != 3       # True    (not equal)
```

## Your mission
| function | example | returns |
|---|---|---|
| `average(a, b, c)` | `average(1, 2, 4)` | `2.3333333333333335` (no rounding) |
| `tip(bill, percent)` | `tip(23.80, 18)` | `4.28` (rounded to 2 decimals) |
| `celsius(fahrenheit)` | `celsius(212)` | `100.0` (rounded to 1 decimal). Formula: (F − 32) × 5 ÷ 9 |
| `clock(seconds)` | `clock(3725)` | `"1:02:05"` (hours:minutes:seconds) |
| `is_even(n)` | `is_even(10)` | `True` |

<details><summary>Hint: tip</summary>

18 percent means 18/100. So the tip is `bill * percent / 100`, then `round(..., 2)`.
</details>

<details><summary>Hint: clock</summary>

3725 seconds is 1 hour (3600), with 125 seconds left over. That's 2 minutes, with 5 seconds left over.
Use `//` to get the hours, `%` to get what's left, and then do the same again for minutes.
Pad minutes and seconds with `:02`. Don't pad hours.
</details>

<details><summary>Hint: is_even</summary>

The comparison `n % 2 == 0` is already `True` or `False`. You can `return` it directly.
</details>

## Level up (not graded)
- Write `clock_to_seconds("1:02:05")` that goes the other way. You'll need `.split(":")` and `int()`.
- Use `input()` to build a tip calculator you can actually use at a restaurant. (`input` always gives you a string, so remember to convert it.)
