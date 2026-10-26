# Mission 8: BOSS: Text Adventure
**BOSS** · 100 xp · your file: `workspace/python/basics/adventure.py`

Time to put everything from this chapter together and build a **game engine**.
Strings, numbers, decisions, loops, lists, dicts and functions all come into play.

When you're done, run the file and **play your own game**.

## The world
The map is already in your file. It's a dict of rooms, and each room is a dict too:
```python
"hall": {
    "desc": "A dusty hall with a flickering torch.",
    "exits": {"north": "library", "east": "kitchen"},
    "items": ["lamp"],
},
```
Hall → north → library. Hall → east → kitchen. Kitchen → down → cellar. There's a locked chest in the cellar.

## What to build
**`new_game()`** returns a fresh game state, a dict with at least:
- `"room"`: the room you're in, starting at `"hall"`
- `"inventory"`: a list of the items you carry, starting empty
- `"won"`: `False`
- the items in each room, as **copies** of the lists in `WORLD`. Taking the lamp in one game must not remove it from the next game.

**`do(state, command)`** carries out one command, updates `state`, and **returns** the message to show.
Commands ignore upper/lower case and extra spaces, so `"  GO   North "` works.

| command | what happens | message |
|---|---|---|
| `look` | | the room description (see below) |
| `go <dir>` | move, if there's an exit that way | the new room's description |
| | no exit that way | `You can't go that way.` |
| | trying to enter the cellar without the lamp | `It's too dark to go down there without a light.` |
| `go` (by itself) | | `Go where?` |
| `take <item>` | the item moves from the room into your inventory | `Taken: lamp.` |
| | the item isn't here | `There is no sword here.` |
| `take` (by itself) | | `Take what?` |
| `inventory` | | `You carry: lamp, key.` (in the order you took them) or `You carry nothing.` |
| `open chest` | not in the cellar | `There is nothing to open here.` |
| | in the cellar, no key | `The chest is locked.` |
| | in the cellar, with the key | `The key turns. Inside the chest: a golden snake. You win!` and set `"won"` to `True` |
| anything else | | `I don't understand that.` |

**Room description** = the description, then the items (only if there are any), then the exits in alphabetical order:
```
A dusty hall with a flickering torch. You see: lamp. Exits: east, north.
Tall shelves of crumbling books. You see: key, book. Exits: south.
It smells like very old soup. Exits: down, west.
```

## How to approach a boss
Don't try to write it all at once.
1. `new_game` and `look` first. Hit Check: some tests pass already. That's progress!
2. Then `go`. Then `take`. Then `inventory`. Then `open`.
3. After each step, play a little in the terminal to try it out.

<details><summary>Hint: splitting the command</summary>

`words = command.lower().split()` turns `"  GO   North "` into `["go", "north"]`. Then `words[0]` is the verb.
Careful: an empty command gives `[]`, and `words[0]` would crash on it.
</details>

<details><summary>Hint: copying the items</summary>

Loop over `WORLD`, and for each room store `list(WORLD[room]["items"])`. `list(...)` makes a new copy of a list.
</details>

<details><summary>Hint: structure</summary>

Write a helper `describe(state)` that builds the room description. Both `look` and `go` need it.
Splitting work into small helper functions is how real programs stay readable.
</details>

## Level up (not graded)
- Add shortcuts: `n`, `s`, `e`, `w`, and `i` for inventory.
- Add `drop <item>`. Add a new room. Add a monster that blocks a door until you `use` the book on it.
- Count moves, and print a score when you win.
