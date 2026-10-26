# Mission 6: Task Tracker
**BUILD** · 125 xp · your file: `workspace/python/kit/tasks.py`

Up to now you've written functions. Now you'll write a **class**: an object that holds its own data
(the tasks) along with the actions that work on it (add, finish, save).

You'll also *raise* errors on purpose. Good code refuses bad input loudly instead of quietly doing something weird.

## What to build: `class TaskList`
| method | does |
|---|---|
| `TaskList()` | an empty list of tasks |
| `.add(title, priority=1)` | adds a task, returns its id. Ids start at 1 and count up |
| `.done(task_id)` | marks a task finished |
| `.pending()` | titles of unfinished tasks: highest priority first, then oldest first |
| `len(tasks)` | number of unfinished tasks |
| `.save(path)` | writes everything to a JSON file |
| `TaskList.load(path)` | builds a TaskList back from that file (a `@classmethod`) |

Rules:
- `priority` must be 1, 2 or 3. Anything else raises `ValueError`.
- A blank title (`""` or `"   "`) raises `ValueError`.
- `.done()` with an id that doesn't exist raises `KeyError`.
- After `load`, new ids keep counting from where they left off. Never reuse an id.

```python
t = TaskList()
t.add("homework", priority=3)   # 1
t.add("clean room")             # 2
t.pending()                     # ['homework', 'clean room']
t.done(1)
len(t)                          # 1
```

Then hit **Check my code**.

<details><summary>Hint 1: storing tasks</summary>

A dict from id to task works well: `self.tasks = {1: {"title": "homework", "priority": 3, "done": False}}`.
Keep `self.next_id` as a separate counter.
</details>

<details><summary>Hint 2: len()</summary>

`len(obj)` calls `obj.__len__()`. Define that method.
</details>

<details><summary>Hint 3: JSON gotcha</summary>

JSON object keys are always strings. Save `{1: ...}`, load it back, and you get `{"1": ...}`.
Convert them back with `int(key)`. Or save the tasks as a list instead of a dict.
</details>

<details><summary>Hint 4: classmethod</summary>

```python
@classmethod
def load(cls, path):
    tasks = cls()      # a fresh TaskList
    ...                # fill it from the file
    return tasks
```
</details>

## Level up (not graded)
- Give it a command line: `python tasks.py add "buy milk" 2`, `python tasks.py list`, `python tasks.py done 3`, all saving to `tasks.json`. Now you have a real todo app.
- Use a `@dataclass` for a single task instead of a dict.

## Docs
- Classes: https://docs.python.org/3/tutorial/classes.html
- json: https://docs.python.org/3/library/json.html
