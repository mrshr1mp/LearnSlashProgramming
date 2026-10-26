# Mission 3: Decision Maker
**LEARN** · 35 xp · your file: `workspace/python/basics/decisions.py`

So far your code does the same thing every time. Now it gets to make **decisions**.

## Lesson: if / elif / else
```python
def describe_temp(t):
    if t > 30:
        return "hot"
    elif t > 15:
        return "nice"
    else:
        return "cold"
```
Python checks each condition **from top to bottom** and runs the **first** one that's true. Then it skips the rest.
So `describe_temp(35)` is `"hot"`. It never gets as far as checking `t > 15`, even though that's true too.

**Order matters.** If you checked `t > 15` first, 35 degrees would come out as `"nice"`.

## Lesson: comparisons
| | means |
|---|---|
| `==` `!=` | equal, not equal |
| `<` `>` `<=` `>=` | less than, greater than, and "or equal" versions |
| `"a" in "cat"` | is this text inside that text? (`True`) |

## Lesson: and, or, not
```python
age = 16
has_ticket = True
age >= 13 and has_ticket     # True: both must be true
age >= 18 or has_ticket      # True: at least one must be true
not has_ticket               # False: flips it
```

## Lesson: string checks
Strings have yes/no methods that are handy for decisions:
```python
"hello".isalpha()    # True: only letters
"12345".isdigit()    # True: only digits
"abc123".isalpha()   # False
```

## Your mission
**`grade(score)`** turns a test score into a letter:
90 and up is `"A"`, 80+ is `"B"`, 70+ is `"C"`, 60+ is `"D"`, and anything lower is `"F"`.
A score below 0 or above 100 gives `"invalid"`.

**`fizzbuzz(n)`** is the classic programming-interview puzzle:
- divisible by both 3 and 5: `"FizzBuzz"`
- divisible by 3: `"Fizz"`
- divisible by 5: `"Buzz"`
- otherwise, the number as a string: `fizzbuzz(7)` gives `"7"`

**`password_strength(pw)`**, with the rules checked in this order:
1. shorter than 8 characters: `"weak"`
2. only letters, or only digits: `"weak"`
3. 12 or more characters: `"strong"`
4. anything else: `"ok"`

**`ticket_price(age, is_student)`**:
under 5 gets in free (`0`), 65 and over pays `6`, under 18 **or** a student pays `8`, and everyone else pays `12`.
A 70-year-old student pays `6`, because the senior rule comes first.

<details><summary>Hint: fizzbuzz</summary>

"Divisible by 3" means `n % 3 == 0`. Check the "both" case **first**. Why? Try putting it last and see what happens to 15.
</details>

<details><summary>Hint: password_strength</summary>

Use `len(pw)`, `pw.isalpha()` and `pw.isdigit()`. Write one `if` per rule, in order, each with its own `return`.
</details>

## Level up (not graded)
- In the `__main__` block, print `fizzbuzz` for every number from 1 to 100. (Loops are next mission. Come back later!)
- Add a rule: a password containing the word `"password"` is always `"weak"`. (Hint: `in`, and `.lower()`.)
