# Mission 6: Dictionary Detective
**LEARN** · 50 xp · your file: `workspace/python/basics/dicts.py`

A list finds things by **position**. A **dictionary** finds things by **name**. Dicts are probably the most-used tool in all of Python.

## Lesson: key → value
```python
ages = {"ada": 36, "alan": 41}
ages["ada"]             # 36
ages["grace"] = 85      # add a new key (or replace an old one)
"alan" in ages          # True  (checks the KEYS)
len(ages)               # 3
```
Asking for a key that isn't there crashes with a `KeyError`. Use `.get` for a fallback:
```python
ages["bob"]             # KeyError!
ages.get("bob")         # None
ages.get("bob", 0)      # 0
```

## Lesson: looping over a dict
```python
for name in ages:                  # loops over the keys
    print(name)

for name, age in ages.items():     # keys AND values together
    print(f"{name} is {age}")

list(ages.keys()), list(ages.values())
```

## Lesson: the counting pattern
This shows up everywhere. Learn it by heart:
```python
counts = {}
for word in ["cat", "dog", "cat"]:
    counts[word] = counts.get(word, 0) + 1
# {'cat': 2, 'dog': 1}
```
On a word's first visit, `.get` gives back 0. After that, it gives back the count so far.

## Lesson: lists inside dicts
Values can be anything, even lists:
```python
teams = {}
teams.setdefault("red", []).append("ada")    # creates the list the first time
teams.setdefault("red", []).append("alan")   # reuses it after that
# {'red': ['ada', 'alan']}
```

## Lesson: sets
A **set** is like a dict with only keys: no duplicates, no order, and really fast `in` checks.
```python
seen = set()
seen.add("x"); seen.add("x")
len(seen)        # 1
set([1, 1, 2])   # {1, 2}
```

## Your mission
| function | example | returns |
|---|---|---|
| `letter_counts(text)` | `letter_counts("Hello!")` | `{"h": 1, "e": 1, "l": 2, "o": 1}` (letters only, lowercased) |
| `invert(d)` | `invert({"a": 1, "b": 2})` | `{1: "a", 2: "b"}` |
| `group_by_length(words)` | `group_by_length(["cat", "horse", "dog"])` | `{3: ["cat", "dog"], 5: ["horse"]}` |
| `restock(inventory, delivery)` | see below | a **new** dict |

`restock` adds a delivery to an inventory. Items in both get their amounts added together, and new items get added:
```python
restock({"apples": 5, "pears": 2}, {"apples": 10, "kiwis": 4})
# {"apples": 15, "pears": 2, "kiwis": 4}
```
**Don't change the dicts you were given.** Make a copy with `dict(inventory)` and change that.

<details><summary>Hint: letter_counts</summary>

The counting pattern, plus `if ch.isalpha():`, plus `.lower()`.
</details>

<details><summary>Hint: group_by_length</summary>

The key is `len(word)`. `setdefault(key, []).append(word)` is the move.
</details>

## Level up (not graded)
- Write `most_common_letter(text)`. `max(counts, key=counts.get)` is a neat trick. Figure out why it works.
- Make a phone book in the `__main__` block: loop on `input()`, where `add ada 555-1234` stores a number and `find ada` looks it up.
