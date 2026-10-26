# Mission 7: Config Merger
**BUILD** · 125 xp · your file: `workspace/python/kit/config.py`

Most real programs have default settings plus your custom settings on top. Merging them
sounds easy until the settings are nested inside each other. This mission is about **recursion**:
a function that calls itself to handle data that contains more of the same kind of data.

```python
defaults = {"db": {"host": "localhost", "port": 5432}, "debug": False}
mine     = {"db": {"port": 6543}, "debug": True}
merge(defaults, mine)
# {"db": {"host": "localhost", "port": 6543}, "debug": True}
```
Note that `host` survived. A plain `{**defaults, **mine}` would throw away the whole `db` dict.

## What to build
- `merge(base, override)` gives a new dict: everything in `base`, updated by `override`.
  - If **both** sides have a dict under the same key, merge those dicts too, as deep as it goes.
  - Otherwise the override value wins (lists get replaced, not combined).
  - **Don't change `base` or `override`.** Changing the result later must not change them either.
- `get(config, path, default=None)` looks up a dotted path: `get(cfg, "db.port")` gives `6543`.
  Missing path? Return `default`. Don't crash.
- `flatten(config)` turns nesting into dotted keys: `{"db.host": "localhost", "db.port": 6543, "debug": True}`

Then hit **Check my code**.

## Think before you code
To merge two dicts, what do you do when a value is itself a pair of dicts?
You... merge them. That's the whole trick. Write that sentence as code.

<details><summary>Hint 1: merge skeleton</summary>

```python
result = dict(base)  # shallow copy, careful
for key, value in override.items():
    if <both are dicts>:
        result[key] = merge(result[key], value)
    else:
        result[key] = value
```
`isinstance(x, dict)` checks for a dict. And the "careful" part: what happens to nested dicts in base that override never touches? Look up `copy.deepcopy`.
</details>

<details><summary>Hint 2: get</summary>

`path.split(".")` then walk down one key at a time. If at any step the current thing isn't a dict, or the key isn't there, return the default.
</details>

<details><summary>Hint 3: flatten</summary>

Give it a hidden extra parameter: `def flatten(config, prefix="")`. When you find a nested dict, call `flatten(value, prefix + key + ".")`.
</details>

## Level up (not graded)
- Write `unflatten`, which turns `{"db.host": "x"}` back into `{"db": {"host": "x"}}`.
- Load the two configs from JSON files and print the merged result.

## Docs
- Recursion explained well: https://realpython.com/python-thinking-recursively/
- `copy`: https://docs.python.org/3/library/copy.html
