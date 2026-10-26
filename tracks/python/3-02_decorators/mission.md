# Mission 2: Decorator Lab
**BUILD** · 175 xp · your file: `workspace/python/deep/decorators.py`

You've seen `@classmethod` and `@dataclass`. Those `@` things are **decorators**: functions that wrap other functions
to add powers to them. Web frameworks, test tools and caching libraries all run on them.
Once you understand decorators, a big chunk of "magic" Python stops being magic.

## Lesson: closures
A function defined inside another function can **remember** the variables around it, even after the outer function has finished:
```python
def make_adder(n):
    def add(x):
        return x + n      # remembers n
    return add

add5 = make_adder(5)
add5(10)    # 15
```
To *change* a remembered variable (not just read it), declare it `nonlocal`:
```python
def make_toggle():
    on = False
    def toggle():
        nonlocal on
        on = not on
        return on
    return toggle
```

## Lesson: *args and **kwargs
`*args` collects any number of positional arguments into a tuple, and `**kwargs` collects keyword arguments into a dict.
Together they let a wrapper accept **anything** and pass it along:
```python
def wrapper(*args, **kwargs):
    return original(*args, **kwargs)
```

## Lesson: decorators
A decorator takes a function and returns a new function that usually calls the old one:
```python
import functools

def loud(func):
    @functools.wraps(func)          # copies the name and docstring over to the wrapper
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result).upper()
    return wrapper

@loud               # exactly the same as writing: greet = loud(greet)
def greet(name):
    return f"hi {name}"

greet("ada")        # 'HI ADA'
```

## Lesson: decorators with arguments
`@repeat(3)` means: call `repeat(3)`, and *that* returns the actual decorator. So it's three functions deep:
```python
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
```

## Your mission
- **`make_counter()`** returns a function. Each call to that function returns the next number: 1, 2, 3...
  Two counters are independent of each other.
- **`@count_calls`** wraps a function and gives the wrapper a `.calls` attribute that counts how many times it's been called.
  It keeps the original `__name__`.
- **`@memoize`** caches results: calling with the same arguments again returns the saved answer without running the function.
  With it, a naive recursive `fib(80)` finishes instantly instead of taking forever. (Positional arguments only is fine.)
- **`@retry(times)`**: if the function raises an exception, try again, up to `times` attempts in total.
  If every attempt fails, raise the last exception.

<details><summary>Hint: count_calls</summary>

Functions are objects, so you can put attributes on them: `wrapper.calls = 0`. Inside the wrapper, do `wrapper.calls += 1`.
</details>

<details><summary>Hint: memoize</summary>

Keep a dict in the closure: `cache = {}`. `args` is a tuple, and tuples can be dict keys. If `args in cache`, return the saved answer.
</details>

<details><summary>Hint: retry</summary>

```python
for attempt in range(times):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        last = e
raise last
```
</details>

## Level up (not graded)
- The standard library already has `@functools.cache`. Compare it with your `memoize`.
- Write `@timer`, which prints how long a function took. Use `time.perf_counter()`.
