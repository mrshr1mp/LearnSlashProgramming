# Mission 5: List Wrangler
**LEARN** · 45 xp · your file: `workspace/python/basics/lists.py`

A **list** holds many values in order. Scores, file names, players, lines of a file: real programs are full of lists.

## Lesson: making and reading lists
```python
scores = [90, 72, 85]
scores[0]          # 90   (first, index 0, same as strings)
scores[-1]         # 85   (last)
len(scores)        # 3
85 in scores       # True
```

## Lesson: changing lists
```python
scores.append(60)      # add to the end: [90, 72, 85, 60]
scores.remove(72)      # remove the first 72: [90, 85, 60]
scores[0] = 95         # replace: [95, 85, 60]
```

## Lesson: slicing
`list[start:stop]` gives a new list from `start` up to (not including) `stop`. It works on strings too.
```python
nums = [10, 20, 30, 40, 50]
nums[1:3]     # [20, 30]
nums[:2]      # [10, 20]       (from the start)
nums[3:]      # [40, 50]       (to the end)
nums[-2:]     # [40, 50]       (last two)
nums[::-1]    # [50, 40, 30, 20, 10]   (reversed! also works on strings)
```

## Lesson: handy built-ins
```python
sum([1, 2, 3])                    # 6
max([4, 9, 2]), min([4, 9, 2])    # 9, 2
sorted([3, 1, 2])                 # [1, 2, 3]   (gives a NEW sorted list)
sorted([3, 1, 2], reverse=True)   # [3, 2, 1]
" + ".join(["a", "b", "c"])       # "a + b + c"  (glue strings in a list together)
```

**Careful:** `nums.sort()` sorts the list *in place* and changes the original. `sorted(nums)` leaves it alone.
If someone passes you a list, changing it can mess up their data. That's a real bug people ship all the time.

## Lesson: building a new list in a loop
The accumulator pattern from mission 4, now with a list:
```python
def evens(nums):
    result = []
    for n in nums:
        if n % 2 == 0:
            result.append(n)
    return result
```

## Your mission
| function | example | returns |
|---|---|---|
| `countdown(n)` | `countdown(3)` | `[3, 2, 1, "Liftoff!"]` |
| `top3(scores)` | `top3([50, 90, 70, 85])` | `[90, 85, 70]`. Must **not** change `scores` |
| `unique(items)` | `unique([3, 1, 3, 2, 1])` | `[3, 1, 2]` (first time each appears, original order) |
| `chunk(items, size)` | `chunk([1, 2, 3, 4, 5], 2)` | `[[1, 2], [3, 4], [5]]` |
| `rotate(items, k)` | `rotate([1, 2, 3, 4], 1)` | `[4, 1, 2, 3]` (move the last k items to the front) |

`rotate` with k bigger than the list should still work: rotating 4 items by 5 is the same as rotating by 1.
An empty list rotates to `[]`.

<details><summary>Hint: top3</summary>

`sorted(..., reverse=True)` then a slice. Fewer than 3 scores? A slice doesn't crash if the list is short. Try it!
</details>

<details><summary>Hint: unique</summary>

Build a new list. Only `append` an item `if item not in result`.
</details>

<details><summary>Hint: chunk</summary>

`range(0, len(items), size)` gives you the start of each chunk: 0, 2, 4... Then slice from there.
</details>

<details><summary>Hint: rotate</summary>

`k % len(items)` turns 5 into 1 for a 4-item list. Then glue two slices together with `+`: the last k items, followed by the rest.
Handle the empty list first: `% 0` crashes.
</details>

## Level up (not graded)
- Write `second_largest(nums)` without using `sorted`.
- Make `unique` fast for a million items. (Spoiler for mission 6: a `set` checks `in` instantly, a list checks one item at a time.)
