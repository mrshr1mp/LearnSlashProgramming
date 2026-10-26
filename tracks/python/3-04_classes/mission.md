# Mission 4: Shape Arena
**BUILD** · 175 xp · your file: `workspace/python/deep/shapes.py`

In the Kit chapter you built a class. Now learn how Python's own types work under the hood,
so your classes can behave like they're built in: `v1 + v2`, `abs(v)`, `sorted(shapes)`, `print(v)`.

## Lesson: dunder methods
"Dunder" means **d**ouble **under**score. Python calls these special methods for you behind the scenes:

| you write | Python calls |
|---|---|
| `a + b` | `a.__add__(b)` |
| `a - b` | `a.__sub__(b)` |
| `a * 3` | `a.__mul__(3)` |
| `3 * a` | `a.__rmul__(3)` (the "reflected" version, used when the left side doesn't know how) |
| `a == b` | `a.__eq__(b)` |
| `a < b` | `a.__lt__(b)` (and then `sorted` just works) |
| `abs(a)` | `a.__abs__()` |
| `repr(a)`, and how it shows up in the REPL | `a.__repr__()` |
| `hash(a)` (needed to go in a set or be a dict key) | `a.__hash__()` |

Heads up: if you define `__eq__`, Python *removes* the default `__hash__`. You have to write your own if you still want hashing.

## Lesson: inheritance
A class can build on another one. It gets all of the parent's methods, and it can override some of them:
```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return "..."
    def intro(self):
        return f"{self.name} says {self.speak()}"   # calls whichever speak() the object really has

class Dog(Animal):
    def speak(self):
        return "Woof"

Dog("Rex").intro()     # 'Rex says Woof'
```
`super().__init__(...)` calls the parent's version of a method. `type(self).__name__` gives the class name as a string.

## Lesson: properties
`@property` makes a method look like an attribute: you write `rect.perimeter` with no `()`. It's computed fresh every time.

## Your mission
**`Vector(x, y)`**, a 2D vector:
- `v.x`, `v.y`
- `Vector(1, 2) + Vector(3, 4) == Vector(4, 6)`, and `-` works the same way
- `Vector(1, 2) * 3 == Vector(3, 6)`, and `3 * Vector(1, 2)` works too
- `abs(Vector(3, 4)) == 5.0` (the length)
- `repr(Vector(1, 2)) == "Vector(1, 2)"`
- hashable: `len({Vector(1, 2), Vector(1, 2)}) == 1`

**`Shape`**, the base class:
- `area()` raises `NotImplementedError` (each kind of shape fills it in)
- `describe()` returns `"Circle with area 3.14"`: the class name and the area to 2 decimals
- shapes compare by area with `<`, so `sorted(shapes)` orders them smallest first

**`Circle(radius)`**, **`Rect(width, height)`** and **`Square(side)`** all inherit from `Shape`.
`Square` inherits from **`Rect`**, and calls `super().__init__(side, side)`.
`Rect` has a `perimeter` **property**.

<details><summary>Hint: __eq__</summary>

```python
def __eq__(self, other):
    return isinstance(other, Vector) and (self.x, self.y) == (other.x, other.y)

def __hash__(self):
    return hash((self.x, self.y))
```
</details>

<details><summary>Hint: area of a circle</summary>

`math.pi * self.radius ** 2`
</details>

## Level up (not graded)
- Add `Vector.dot(other)` and `Vector.normalized()`.
- Look up `functools.total_ordering`. It fills in `<=`, `>`, and `>=` from `__lt__` and `__eq__`.
- Look up `abc.ABC` and `@abstractmethod`. Then nobody can make a plain `Shape()` by accident.
