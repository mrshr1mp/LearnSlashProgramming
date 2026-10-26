# Mission 9: FINAL BOSS: Interpreter
**BOSS** · 400 xp · your file: `workspace/python/deep/calc.py` (it starts empty)

Build a **programming language**. A small one: a calculator with variables. But it works the same way as Python itself:
read text, break it into pieces, understand its structure, and compute an answer.

**`eval()` and `exec()` are banned.** The tests check. You're building the thing that `eval` does.

## What to build
```python
calc = Calculator()
calc.run("2 + 3 * 4")          # 14         (* before +)
calc.run("(2 + 3) * 4")        # 20
calc.run("10 / 4")             # 2.5
calc.run("8 - 3 - 2")          # 3          (left to right: (8 - 3) - 2)
calc.run("2 ^ 3 ^ 2")          # 512        (power goes RIGHT to left: 2 ^ (3 ^ 2))
calc.run("-3 + 5")             # 2          (unary minus)
calc.run("2 * -(1 + 2)")       # -6
calc.run("let x = 5")          # 5          (stores x, returns its value)
calc.run("let y = x * 2 + 1")  # 11
calc.run("x + y")              # 16
calc.run("1.5 * 2")            # 3.0
```
Spaces are optional everywhere: `"2*(3+4)"` works too. Variable names are letters and `_`.

**Errors**: define `class CalcError(Exception)`, and raise it (never anything else) for:
- unknown variables: `"z + 1"`
- division by zero: `"1 / 0"`
- broken syntax: `"2 +"`, `"(1 + 2"`, `"1 + 2)"`, `"2 3"`, `"3 $ 4"`, `""`, `"let = 5"`, `"let 5 = x"`

## How real interpreters work
1. **Tokenizer:** turns `"2*(x+10)"` into `[2, "*", "(", "x", "+", 10, ")"]`.
2. **Parser:** reads the tokens and respects precedence. The classic method is **recursive descent**:
   one function per precedence level, where each one calls the level below it.
3. **Evaluate** as you parse (simplest), or build a tree first and evaluate it afterwards (more powerful).

That's the grammar for this calculator. Each line is one function:
```
expression := term   (("+" | "-") term)*
term       := unary  (("*" | "/") unary)*
unary      := "-" unary  |  power
power      := atom   ("^" unary)?          <- right side calls back up, which makes it right-to-left
atom       := NUMBER | NAME | "(" expression ")"
```

No more hints. This is the one where you find out what you can do. Take your time.
It's fine to spend several sessions on it. Get `"1 + 2"` working first, then grow it.

## When you beat it
You built a tokenizer, a recursive-descent parser and an evaluator, with error handling. Those are the same pieces inside every compiler.
**You know Python.** Say it with your chest.

Where to go next:
- Add functions to your language: `let sq(n) = n * n`.
- Read *Crafting Interpreters* (free online at craftinginterpreters.com) and keep going.
- Advent of Code. Real projects. Things nobody assigned you.
- Ready for another language? Add a new track in `tracks/`. Your Python skills carry over.
