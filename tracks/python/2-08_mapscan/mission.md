# Mission 8: Island Counter
**PUZZLE** · 150 xp · your file: `workspace/python/kit/mapscan.py`

A satellite sent back a map. `#` is land, `.` is water:
```
##..#
#...#
..#..
.....
##.##
```
An **island** is a group of land cells connected up, down, left or right (diagonals don't count).
This map has 5 islands, with sizes 3, 2, 2, 2 and 1.

`samples/map.txt` is a much bigger map. **How many islands does it have, and how big is the biggest?**

This is the kind of puzzle in Advent of Code (adventofcode.com), which is a great place to go after this app.

## What to build
- `parse(text)` turns the map text into a list of row strings. Ignore blank lines and stray spaces at line ends.
- `islands(grid)` returns the size of every island, biggest first: `[3, 2, 2, 2, 1]`. No land gives `[]`.

## The catch
The tests include a 300×300 map that's solid land: one island of 90,000 cells.
The most obvious solution crashes on it. If yours does, read the error. It tells you exactly what went wrong.

Then hit **Check my code**.

<details><summary>Hint 1: the idea</summary>

Go through every cell. When you hit land you haven't seen yet, that's a new island: explore from there
and mark everything connected as "seen", counting as you go. Keep the "seen" cells in a `set` of `(row, col)` tuples.
</details>

<details><summary>Hint 2: exploring</summary>

Keep a to-do list of cells to visit. Pop one, count it, push its unseen land neighbours. Repeat until the list is empty.
That's a flood fill. With `collections.deque` and `popleft()` it's called breadth-first search (BFS).
</details>

<details><summary>Hint 3: RecursionError?</summary>

If your explore function calls itself for each neighbour, Python gives up after about 1000 nested calls.
Use the to-do-list approach from hint 2 instead: no recursion needed.
</details>

## Level up (not graded)
- Diagonals count too. How small is the change to your code?
- Print the map with the biggest island drawn in `@`.

## Docs
- deque: https://docs.python.org/3/library/collections.html#collections.deque
- Sets: https://docs.python.org/3/tutorial/datastructures.html#sets
