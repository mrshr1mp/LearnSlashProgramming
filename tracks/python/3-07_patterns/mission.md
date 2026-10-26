# Mission 7: Pattern Hunter
**BUILD** · 175 xp · your file: `workspace/python/deep/patterns.py`

**Regular expressions** are a mini-language for describing text patterns, like "four digits, a dash, two digits".
They look like line noise at first. They're also one of the highest-value skills in automation:
searching logs, cleaning data, validating input. Every language has them, and the syntax is nearly identical everywhere.

## Lesson: the building blocks
| pattern | matches |
|---|---|
| `abc` | exactly "abc" |
| `.` | any single character |
| `\d` `\w` `\s` | a digit, a "word" character (letter/digit/_), whitespace |
| `[aeiou]` `[a-z]` `[^0-9]` | one of these, a range, NOT one of these |
| `x*` `x+` `x?` | 0 or more, 1 or more, 0 or 1 |
| `x{3}` `x{2,4}` | exactly 3, between 2 and 4 |
| `^` `$` | start of text, end of text |
| `(...)` | a group: capture this part |
| `a\|b` | a or b |
| `\b` | a word boundary |

Always write patterns as **raw strings**: `r"\d+"`. Without the `r`, Python treats backslashes specially first.

## Lesson: the re module
```python
import re
re.findall(r"\d+", "3 cats, 12 dogs")          # ['3', '12']
re.search(r"(\d+) dogs", "3 cats, 12 dogs")[1]  # '12'   (the group's text)
re.fullmatch(r"[a-z]+", "hello")               # a match (the WHOLE string must match), or None
re.sub(r"\d", "#", "pin 1234")                 # 'pin ####'
re.findall(r"cat", "Cat CAT", re.IGNORECASE)   # ['Cat', 'CAT']
```
If a pattern has groups, `findall` returns just the groups. Named groups make a match easier to read:
```python
m = re.fullmatch(r"(?P<h>\d+):(?P<m>\d\d)", "9:05")
m["h"], m["m"]      # ('9', '05')
```
`re.sub` can take a **function** instead of a replacement string. It gets each match and returns that match's replacement.

Practice on **regex101.com**. Pick the Python flavor. It explains every piece of your pattern as you type.

## Your mission
| function | example | returns |
|---|---|---|
| `find_dates(text)` | `"due 2026-03-14, not 2026-13-01"` | `["2026-03-14"]` (YYYY-MM-DD with month 01–12 and day 01–31) |
| `hashtags(text)` | `"#Python is fun #python #code_daily"` | `["python", "code_daily"]` (lowercased, no repeats, in order) |
| `valid_username(name)` | `"ada_99"` | `True`: 3 to 16 letters, digits or `_`, starting with a letter |
| `parse_time(text)` | `"3:07 pm"` | `907`: minutes since midnight |
| `redact_numbers(text)` | `"card 1234 5678, pin 12"` | `"card #### ####, pin 12"`: runs of 4+ digits become `#` |

`parse_time` details:
- 24-hour `"15:07"` (hours 0–23) and 12-hour `"3:07 pm"` / `"12:30AM"` (hours 1–12, am/pm in any case, space optional) both work.
- Minutes are always 2 digits. `12:xx am` is just after midnight, and `12:xx pm` is just after noon.
- Anything invalid returns `None`: `"25:00"`, `"13:00 pm"`, `"12:60"`, `"3:7"`, `"noon"`.

<details><summary>Hint: find_dates</summary>

`\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])`. Careful: with groups, `findall` returns the groups instead of the whole match.
Use non-capturing groups `(?:...)`, or use `re.finditer` and `m[0]`.
Also add `\b` at both ends, so you don't grab a piece of a longer number.
</details>

<details><summary>Hint: parse_time</summary>

`(\d{1,2}):(\d{2})\s*([ap]m)?` with `re.fullmatch` and `re.IGNORECASE`. Then check the hour ranges in normal Python. Not everything has to be regex!
</details>

<details><summary>Hint: redact_numbers</summary>

`re.sub(r"\d{4,}", lambda m: "#" * len(m[0]), text)`
</details>

## Level up (not graded)
- Go back to Log Detective (Kit, mission 1) and rewrite `parse_line` as one regex with named groups.
- Write a regex that pulls every URL out of a web page's HTML.
