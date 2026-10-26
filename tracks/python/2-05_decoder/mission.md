# Mission 5: Codebreaker
**PUZZLE** · 125 xp · your file: `workspace/python/kit/decoder.py`

`samples/secret.txt` is a scrambled message. It uses a Caesar cipher: every letter is shifted
the same number of places down the alphabet (shift 3: `a→d`, `b→e`, ... `z→c`). Julius Caesar used it 2000 years ago.

You don't know the shift. Your program has to figure it out.

## What to build
- `shift(text, n)` shifts every letter by `n`, wrapping around `z→a`.
  - Keep upper/lower case: `shift("Hello, World!", 3)` gives `"Khoor, Zruog!"`
  - Anything that isn't a letter stays as it is.
  - `n` can be negative or bigger than 26.
- `crack(ciphertext)` returns the shift that was used to scramble it, so `shift(ciphertext, -crack(ciphertext))` is readable English.

## The puzzle part
There are only 26 possible shifts. Trying them all is easy. The real question is:
**how does a program tell which of 26 outputs "looks like English"?** No hints in this section. Think about it first.

## Try it
Decode `samples/secret.txt`. The message has something to tell you.

Then hit **Check my code**.

<details><summary>Hint 1: shifting one letter</summary>

`ord("a")` is 97, `chr(97)` is `"a"`. Turn the letter into 0-25, add `n`, wrap with `% 26`, turn it back.
`%` handles negative numbers correctly in Python: `-1 % 26 == 25`.
</details>

<details><summary>Hint 2: scoring English (idea A)</summary>

Count how many words of the decoded text are common English words: "the", "and", "is", "of", "to", "you"...
The best shift has the most hits.
</details>

<details><summary>Hint 3: scoring English (idea B)</summary>

Letter frequency. In English, `e` is the most common letter, then `t`, `a`, `o`...
Score each candidate by how often it uses the common letters. This works even with no spaces in the message.
</details>

## Level up (not graded)
- Do both scoring ideas and compare. Which one breaks on really short messages?
- Look up the Vigenère cipher: it shifts each letter by a different amount, driven by a keyword. Build `vigenere(text, key)`.

## Docs
- `ord` / `chr`: https://docs.python.org/3/library/functions.html#ord
- `str.isalpha`, `str.isupper`: https://docs.python.org/3/library/stdtypes.html#str.isalpha
