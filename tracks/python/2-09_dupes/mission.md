# Mission 9: Duplicate Hunter
**BUILD** · 150 xp · your file: `workspace/python/kit/dupes.py`

Everyone has the same photo saved 4 times in different folders. Build a tool that finds files with
identical **contents**, even when their names are different.

Comparing every file against every other file byte by byte is slow. Instead, compute a **hash** of each file:
a short fingerprint like `2cf24dba5fb0a30e...`. Same contents always give the same hash.
So "find duplicates" becomes "group files by hash", which you already know how to do from mission 2.

## What to build
- `file_hash(path)` returns the SHA-256 hash of the file's contents as a hex string.
  Read the file in **chunks** (say 64 KB at a time), not all at once. A 4 GB video shouldn't need 4 GB of RAM.
- `walk_files(folder)` is a **generator** that yields every file (not folder) inside `folder`, including inside subfolders.
- `find_dupes(folder)` returns a list of groups. Each group is a list of 2 or more paths with identical contents.
  Sort the paths inside each group, and sort the groups.

## Generators?
A normal function builds the whole list and then returns it. A generator hands out items one at a time, as they're asked for:
```python
def count_up(n):
    for i in range(n):
        yield i        # pause here, hand out i, resume on the next request
```
Walking a drive with a million files, that's the difference between starting instantly and waiting a minute.

## Try it
`samples/backup/` has some sneaky duplicates. Find them all.

Then hit **Check my code**.

<details><summary>Hint 1: hashing</summary>

```python
h = hashlib.sha256()
h.update(some_bytes)   # call this once per chunk
h.hexdigest()
```
Open the file with `open(path, "rb")` (read bytes), and `f.read(65536)` gives the next chunk, or `b""` at the end.
</details>

<details><summary>Hint 2: walking</summary>

`Path(folder).rglob("*")` goes through everything recursively. Keep the files, `yield` each one.
</details>

<details><summary>Hint 3: grouping</summary>

A dict from hash to list of paths. `dict.setdefault(key, []).append(path)` or `collections.defaultdict(list)`.
Then keep only the lists with 2 or more paths.
</details>

## Level up (not graded)
- Speed it up: files with different sizes can't be duplicates. Group by `path.stat().st_size` first, and only hash files that share a size.
- Add `--delete`, which keeps the first file of each group and deletes the rest. (Ask before deleting! Use `input()`.)

## Docs
- hashlib: https://docs.python.org/3/library/hashlib.html
- Generators: https://docs.python.org/3/howto/functional.html#generators
