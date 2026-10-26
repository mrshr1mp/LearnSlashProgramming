# Mission 1: Hello, Python
**LEARN** · 25 xp · your file: `workspace/python/basics/hello.py`

Welcome. Every mission in this chapter has two halves: a short **lesson**, then a **mission** where you write real code.
Don't just read the lesson. Type the examples and run them. Your fingers learn faster than your eyes.

## Lesson: running Python
There are two ways to run Python, and you'll use both all the time.

**1. The REPL** (for quick experiments). Open a terminal in VS Code (`` Ctrl+` ``), type `python`, and press Enter.
You get a `>>>` prompt. Type code and see the answer right away:
```python
>>> 2 + 2
4
>>> "ha" * 3
'hahaha'
```
Type `exit()` to leave.

**2. A file** (for real programs). Write code in a `.py` file and run it with the ▶ button in the top right of VS Code,
or type `python hello.py` in the terminal.

## Lesson: variables and strings
A **variable** is a name that holds a value. A **string** is text inside quotes.
```python
name = "Ada"
age = 36
print(name)            # Ada
print(len(name))       # 3  (how many characters)
print(name.upper())    # ADA
print(name + "!")      # Ada!  (+ glues strings together)
```

An **f-string** puts variables straight into text. Put an `f` before the quote and the variable in `{}`:
```python
print(f"{name} is {age} years old")   # Ada is 36 years old
```

You can grab single characters by **index**. Counting starts at 0:
```python
word = "python"
word[0]    # 'p'
word[1]    # 'y'
word[-1]   # 'n'  (negative counts from the end)
```

And `.split()` chops a string into pieces at the spaces:
```python
"ada lovelace".split()      # ['ada', 'lovelace']
"ada lovelace".split()[1]   # 'lovelace'
```

## Lesson: functions
A **function** is a named recipe. You give it inputs, it gives back an answer with `return`:
```python
def double(n):
    return n * 2

double(5)    # 10
```
The indented lines are the function's body. Indentation matters in Python: it's how Python knows what's inside.

**`print` vs `return`:** `print` shows something on screen. `return` hands a value back to whoever called the function.
The checker calls your functions and looks at what they **return**, so always `return` your answer.

## Your mission
Open `hello.py`. `greet` is already done as an example. Write the other three:

| function | example | returns |
|---|---|---|
| `greet(name)` | `greet("Ada")` | `"Hello, Ada!"` (done for you) |
| `shout(text)` | `shout("hey there")` | `"HEY THERE!"` |
| `introduce(name, age)` | `introduce("Ada", 36)` | `"Hi, I'm Ada and I'm 36 years old."` |
| `initials(full_name)` | `initials("ada lovelace")` | `"A.L."` |

Replace each `raise NotImplementedError` with your code. Then hit **Check my code**.

<details><summary>Hint: shout</summary>

`text.upper()` gives the uppercase version. Then add `"!"` with `+`.
</details>

<details><summary>Hint: introduce</summary>

Use an f-string: `f"Hi, I'm {name} and ..."`. Watch the punctuation: the checker wants it exactly.
</details>

<details><summary>Hint: initials</summary>

Split the name into two words. Take the first character (`[0]`) of each, uppercase it, and glue it all together with dots.
For example, `first = full_name.split()[0]`.
</details>

## Level up (not graded)
- Make `initials` work for any number of names: `"grace brewster murray hopper"` gives `"G.B.M.H."` (you'll learn loops in mission 4, come back then).
- At the bottom of the file, under `if __name__ == "__main__":`, use `input("What's your name? ")` to ask for a name and print a greeting.
