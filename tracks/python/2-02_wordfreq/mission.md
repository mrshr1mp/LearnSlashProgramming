# Mission 2: Word Counter
**FILL** · 75 xp · your file: `workspace/python/kit/wordfreq.py`

Kit tool #2: point it at any text and it tells you which words show up most.
The function signatures are written for you. The insides are not.

## What it should do
- `words(text)` returns every word, lowercased, in order. A word is a run of letters `a-z` and apostrophes,
  so `"Don't PANIC, ok?"` gives `["don't", "panic", "ok"]`.
- `top_words(text, n=10, ignore=())` returns the `n` most common words as `[(word, count), ...]`.
  - Most common first. **Ties go alphabetically.**
  - Words listed in `ignore` don't count at all.

```python
>>> top_words("The cat and the hat. THE END, and that's that!", n=3)
[('the', 3), ('and', 2), ('cat', 1)]
```
`cat`, `end`, `hat`, `that`, `that's` all have 1. `cat` wins because it comes first alphabetically.

## Try it
```
python workspace/python/kit/wordfreq.py
```
runs it on `samples/zen.txt` (the Zen of Python; type `import this` in a REPL for the story behind it).

Then hit **Check my code**.

## New tool: the REPL
Stop writing a whole file and then running it. Test one piece at a time:
```
cd workspace/python/kit
python
>>> import wordfreq
>>> wordfreq.words("Hi there, hi!")
```
After you edit the file, `import importlib; importlib.reload(wordfreq)` picks up the changes.

<details><summary>Hint 1: splitting into words</summary>

Two ways. Loop over each character and build words yourself (good practice), or use regular expressions:
`re.findall(r"[a-z']+", text.lower())`. Try both.
</details>

<details><summary>Hint 2: counting</summary>

A dict works: `counts[w] = counts.get(w, 0) + 1`. Or `collections.Counter(list_of_words)` does it in one line.
</details>

<details><summary>Hint 3: ties</summary>

`Counter.most_common()` won't break ties alphabetically. Sort it yourself.
`sorted` can sort by a tuple: `key=lambda pair: (-pair[1], pair[0])` means "count, biggest first, then word A-Z".
</details>

## Level up (not graded)
- Take a filename from `sys.argv` so you can run it on any file.
- Add a `--min-length` option that skips short words like "a" and "is".

## Docs
- `re`: https://docs.python.org/3/library/re.html
- `collections.Counter`: https://docs.python.org/3/library/collections.html#collections.Counter
