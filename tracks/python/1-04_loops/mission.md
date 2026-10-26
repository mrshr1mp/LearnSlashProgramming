# Mission 4: Loop Machine
**LEARN** · 40 xp · your file: `workspace/python/basics/loops.py`

Loops are where programming gets its superpower: doing something a million times costs you no extra typing.

## Lesson: for loops
A `for` loop runs its body once for each item:
```python
for letter in "cat":
    print(letter)      # c, then a, then t
```

`range` gives you numbers to loop over:
```python
range(5)         # 0, 1, 2, 3, 4   (stops BEFORE 5)
range(1, 6)      # 1, 2, 3, 4, 5
range(10, 0, -2) # 10, 8, 6, 4, 2  (start, stop, step)

for i in range(3):
    print("hi", i)     # hi 0, hi 1, hi 2
```

## Lesson: the accumulator pattern
This is the most useful loop trick there is: start with an empty result, and add to it every time around.
```python
def total(n):
    result = 0                 # 1. start empty
    for i in range(1, n + 1):
        result = result + i    # 2. add to it each time (shortcut: result += i)
    return result              # 3. return it AFTER the loop finishes

total(4)    # 1 + 2 + 3 + 4 = 10
```
It works for strings too: start with `""` and add characters.

Classic bug: putting the `return` *inside* the loop, indented. Then the function returns on the very first pass.

## Lesson: while loops
`while` keeps going as long as a condition is true. Use it when you don't know ahead of time how many steps it'll take:
```python
n = 100
steps = 0
while n > 1:
    n = n // 2
    steps += 1
# steps is now 6
```
If the condition never becomes false, the loop runs forever. (The checker stops it after 60 seconds.
In a terminal, press Ctrl+C to stop it.)

## Your mission
| function | example | returns |
|---|---|---|
| `sum_to(n)` | `sum_to(4)` | `10` (1+2+3+4) |
| `count_vowels(text)` | `count_vowels("Programming")` | `3` (a, e, i, o, u, upper or lower case) |
| `reverse(text)` | `reverse("loop")` | `"pool"`. Use a loop! |
| `stars(n)` | `stars(3)` | `"*\n**\n***"` (a triangle, one row per line) |
| `collatz_steps(n)` | `collatz_steps(6)` | `8` |

**Collatz** is a famous unsolved math puzzle. Start with any number. If it's even, halve it. If it's odd, multiply by 3 and add 1.
Repeat until you reach 1. Count the steps:
`6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1` is 8 steps. Nobody has ever proved that every number reaches 1. Try 27!

<details><summary>Hint: count_vowels</summary>

Accumulator: `count = 0`, then loop over the letters. For each letter, `if letter.lower() in "aeiou": count += 1`.
</details>

<details><summary>Hint: reverse</summary>

Accumulator with a string: start with `result = ""`. For each letter, put it in **front**: `result = letter + result`.
</details>

<details><summary>Hint: stars</summary>

Build each row with `"*" * i`. Collect the rows into a string with `"\n"` between them, but not after the last one.
(You'll meet a much neater tool for this in mission 5: `"\n".join(...)`.)
</details>

## Level up (not graded)
- Which number below 1000 takes the most Collatz steps? Write a loop to find out.
- Print a times table grid from 1×1 to 10×10 using a loop inside a loop.
