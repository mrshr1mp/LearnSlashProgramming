# Mission 3: Infinite Streams
**BUILD** · 175 xp · your file: `workspace/python/deep/streams.py`

How does a `for` loop actually work? And how can you loop over something that never ends, like every prime number,
without running out of memory? This mission opens up the engine.

## Lesson: the iterator protocol
A `for` loop really does this:
```python
it = iter(things)        # ask for an iterator
while True:
    try:
        item = next(it)  # get the next item...
    except StopIteration:
        break            # ...until it says it's done
    ...
```
Anything with an `__iter__` method can be looped over. Here's a class that counts down:
```python
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):                  # a generator method: easiest way to do it
        n = self.start
        while n > 0:
            yield n
            n -= 1
```
Because `__iter__` starts a fresh generator each time, you can loop over the same `Countdown` twice.

## Lesson: generators can be infinite
A generator only computes the next value when you ask for one. So an infinite one is perfectly fine,
as long as you only *take* a few values:
```python
def naturals():
    n = 1
    while True:          # never ends, and that's OK
        yield n
        n += 1

from itertools import islice
list(islice(naturals(), 5))    # [1, 2, 3, 4, 5]
```
`list(naturals())` would run forever, so never do that.

## Lesson: itertools, the stream toolkit
```python
from itertools import islice, count, takewhile, chain
islice(it, 3)                       # first 3 items
count(10)                           # 10, 11, 12, ... forever
takewhile(lambda x: x < 5, it)      # items until one fails the test
chain([1, 2], [3])                  # 1, 2, 3
```
`collections.deque(maxlen=n)` is a list that automatically drops old items once it's full. Handy for sliding windows.

## Your mission
- **`Countdown(n)`**: iterable, gives n, n−1, ..., 1, and can be looped over more than once.
- **`fibonacci()`**: infinite generator: 0, 1, 1, 2, 3, 5, 8...
- **`primes()`**: infinite generator of prime numbers: 2, 3, 5, 7, 11...
- **`take(n, iterable)`**: a list of the first n items. Must work on infinite streams.
- **`window(iterable, size)`**: generator of sliding windows as tuples.
  `window([1, 2, 3, 4], 2)` gives `(1, 2), (2, 3), (3, 4)`. Must be lazy: it has to work on an infinite stream.
- **`chunked(iterable, n)`**: generator of lists of up to n items.
  `chunked(range(7), 3)` gives `[0, 1, 2], [3, 4, 5], [6]`. Also lazy.

<details><summary>Hint: primes</summary>

Keep a list of the primes found so far. A number is prime if no earlier prime up to its square root divides it.
`all(n % p for p in found if p * p <= n)` is close. Watch out, because that `all` checks *every* found prime. Use `takewhile` to stop early.
</details>

<details><summary>Hint: window</summary>

`it = iter(iterable)`, then fill a `deque(maxlen=size)`. Every time it's full, `yield tuple(d)`.
</details>

<details><summary>Hint: chunked</summary>

Loop: `batch = list(islice(it, n))`. If it's empty, stop. Otherwise yield it.
</details>

## Level up (not graded)
- `yield from` hands control to another generator. Use it to write a recursive generator that walks a nested list.
- Write a generator pipeline: read a huge file line by line, filter, transform, take 10. It uses almost no memory.
