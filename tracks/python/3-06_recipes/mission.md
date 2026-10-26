# Mission 6: Recipe Box
**BUILD** · 175 xp · your file: `workspace/python/deep/recipes.py`

Most classes are mainly *data with a few methods*. Writing `__init__`, `__repr__` and `__eq__` by hand every time gets old fast.
**Dataclasses** write them for you. This is how modern Python code models data.

## Lesson: @dataclass
```python
from dataclasses import dataclass, field

@dataclass
class Player:
    name: str
    score: int = 0
    badges: list[str] = field(default_factory=list)

p = Player("ada")
p                     # Player(name='ada', score=0, badges=[])   free __repr__
p == Player("ada")    # True                                      free __eq__
```
The `name: str` parts are **type hints**. They document what a field should hold. Python doesn't enforce them at runtime,
but VS Code uses them to warn you and to autocomplete.

**Classic trap:** `badges: list = []` would make every Player *share one list*. Dataclasses refuse to let you do that.
`field(default_factory=list)` builds a fresh list for each object.

## Lesson: frozen and __post_init__
```python
@dataclass(frozen=True)          # can't be changed after creation (and it's hashable)
class Point:
    x: float
    y: float

    def __post_init__(self):     # runs right after the generated __init__: a good place to validate
        if self.x < 0:
            raise ValueError("x must be >= 0")
```
`dataclasses.replace(p, x=5)` gives a modified copy of a frozen object.

## Lesson: Enum
A fixed set of named choices, so a typo like `"gramm"` can't sneak in:
```python
from enum import Enum

class Size(Enum):
    SMALL = "s"
    LARGE = "l"

Size.SMALL.value     # 's'
Size("l")            # Size.LARGE   (look one up by its value)
```

## Your mission
- **`Unit`**: an Enum with `GRAM = "g"`, `ML = "ml"`, `PIECE = "pc"`.
- **`Ingredient(name, amount, unit)`**: a **frozen** dataclass. An amount ≤ 0 raises `ValueError`.
- **`Recipe(name, servings, ingredients=[])`**: a dataclass (use `default_factory`!). Methods:
  - `scale(servings)` returns a **new** Recipe for that many servings, with every amount scaled and rounded to 2 decimals. The original stays the same.
  - `to_json()` returns a JSON string, and `Recipe.from_json(text)` (a classmethod) rebuilds an equal Recipe from it.
- **`shopping_list(*recipes)`** merges ingredients across recipes into `{name: (total_amount, Unit)}`.
  The same name with different units raises `ValueError`.

```python
pancakes = Recipe("pancakes", 2, [Ingredient("flour", 200, Unit.GRAM), Ingredient("egg", 2, Unit.PIECE)])
pancakes.scale(3).ingredients[0]     # Ingredient(name='flour', amount=300.0, unit=<Unit.GRAM: 'g'>)
```

<details><summary>Hint: to_json</summary>

`dataclasses.asdict(recipe)` turns it into nested dicts, but the `Unit` enums aren't JSON-friendly.
Build the dict yourself, writing `unit.value` instead, then `json.dumps(...)`. In `from_json`, turn the value back with `Unit(value)`.
</details>

<details><summary>Hint: scale</summary>

`factor = servings / self.servings`. Build new Ingredients (they're frozen, so you can't change the old ones), then return `Recipe(self.name, servings, new_list)`.
</details>

## Level up (not graded)
- Add `@dataclass(order=True)` to something, and see what sorting does.
- Look up `typing.Protocol` and `mypy`. Running `mypy` on your file checks the type hints for real.
