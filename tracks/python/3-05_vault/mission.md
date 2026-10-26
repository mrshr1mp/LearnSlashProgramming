# Mission 5: Bank Vault
**BUILD** · 200 xp · your file: `workspace/python/deep/vault.py`

With money, a half-finished operation is a disaster. If a transfer takes money out of one account and then crashes
before it's added to the other, that money is gone. This mission is about code that fails **safely**.

## Lesson: your own exceptions
Make an exception class by inheriting from `Exception`. Build a family of them, so callers can catch exactly what they care about:
```python
class GameError(Exception):
    pass

class OutOfLives(GameError):
    def __init__(self, level):
        super().__init__(f"died on level {level}")   # the message
        self.level = level                            # extra info for whoever catches it

try:
    raise OutOfLives(3)
except GameError as e:      # catches OutOfLives too, because it's a kind of GameError
    print(e, e.level)
```

## Lesson: try / except / else / finally
```python
try:
    risky()
except ValueError:
    ...          # runs only if a ValueError happened
else:
    ...          # runs only if NOTHING went wrong
finally:
    ...          # ALWAYS runs, error or not (cleanup goes here)
```
A bare `raise` inside an `except` block re-raises the same error after you've cleaned up.

## Lesson: context managers (`with`)
`with open(...) as f:` closes the file even if your code crashes. You can build your own `with` objects.

**Way 1: a class** with `__enter__` and `__exit__`:
```python
class Shouting:
    def __enter__(self):
        print("START")
        return self                      # this is what `as x` gets
    def __exit__(self, exc_type, exc, tb):
        print("END")                     # runs even if the block raised
        return False                     # False means "don't swallow the error"
```
If the block raised, `exc_type` is the exception's class. Otherwise it's `None`.

**Way 2: a generator** with `@contextmanager`:
```python
from contextlib import contextmanager

@contextmanager
def shouting():
    print("START")
    try:
        yield                # the with-block runs here
    finally:
        print("END")         # always runs
```

## Your mission
**Exceptions:**
- `BankError(Exception)`, the family name
- `InsufficientFunds(BankError)`, with a `.needed` attribute: how much money is missing
- `AccountLocked(BankError)`

**`Account(owner, balance=0)`** with `.owner`, `.balance` and `.locked` (starts `False`):
- `deposit(amount)`: `ValueError` if amount ≤ 0, `AccountLocked` if locked
- `withdraw(amount)`: `ValueError` if amount ≤ 0, `AccountLocked` if locked, `InsufficientFunds` if there isn't enough.
  Withdrawing 100 from a balance of 30 means `.needed == 70`.

**`transfer(src, dst, amount)`** moves money between accounts. It's **all or nothing**:
if anything fails (src too poor, src locked, **dst locked**), both balances end up exactly as they were, and the error is raised.

**`Transaction(account)`**, a class context manager: it remembers the balance on entry.
If the block raises, it puts the balance back and lets the error continue.

**`frozen(account)`**, a `@contextmanager`: it locks the account inside the block and puts `.locked` back to what it was afterwards, even after an error.

<details><summary>Hint: transfer</summary>

Withdraw first. Then `try:` to deposit. `except BankError:` put the money back into src (it was never actually spent), then `raise`.
</details>

<details><summary>Hint: Transaction</summary>

`__enter__` saves `self.saved = self.account.balance`. `__exit__` checks `if exc_type is not None:` and restores it.
</details>

## Level up (not graded)
- Keep a history list on each account, and print a statement.
- Look up `raise NewError(...) from e`, which chains one exception to another so the original cause isn't lost.
