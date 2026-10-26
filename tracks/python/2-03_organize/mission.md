# Mission 3: Folder Janitor
**BUILD** · 100 xp · your file: `workspace/python/kit/organize.py`

Your Downloads folder is a disaster. Build a tool that sorts files into subfolders by type.
This time you only get the function names. How you write the insides is up to you.

## The rules
| folder   | extensions |
|----------|------------|
| `images` | .jpg .jpeg .png .gif |
| `docs`   | .pdf .txt .docx .md |
| `audio`  | .mp3 .wav |
| `code`   | .py .js .html .css |
| `other`  | anything else, including files with no extension |

- Extensions are case-insensitive: `PARTY.JPG` is an image.
- Only files get moved. Leave folders alone.

## What to build
- `plan(folder)` returns `{filename: destination_folder_name}` for every file directly inside `folder`.
  It must **not** move anything. Example: `{"song.mp3": "audio", "notes.txt": "docs"}`
- `organize(folder, dry_run=True)` returns the same plan. Only when `dry_run=False` does it actually move the files, creating the subfolders if needed.
- **Never overwrite.** If `images/cat.png` already exists, move the new one to `images/cat (1).png`
  (then `cat (2).png`, and so on).

`dry_run` is how real tools work: show what you *would* do before doing anything you can't undo.

## Try it
`samples/messy/` is a pretend messy folder. Run your tool on it with `dry_run=True` first, then for real.
If you wreck it, delete `samples/messy` and run `python learn.py start N` in a terminal (N = this mission's number in the sidebar). That restores the samples and never touches your code.

Then hit **Check my code**.

<details><summary>Hint 1: the right module</summary>

`pathlib` does nearly everything here. `Path(folder).iterdir()` lists a folder, `p.is_file()`, `p.suffix` gives `".JPG"`, `p.stem` gives `"PARTY"`.
To move a file: `p.rename(new_path)` or `shutil.move`.
</details>

<details><summary>Hint 2: the extension table</summary>

Flip it into a lookup dict: `{".jpg": "images", ".png": "images", ...}`. Then use `table.get(ext, "other")`.
You can build that dict from a smaller one with a loop instead of typing every line.
</details>

<details><summary>Hint 3: not overwriting</summary>

`while dest.exists():` keep counting up and building `f"{stem} ({i}){suffix}"`.
</details>

## Level up (not graded)
- Add a `--undo` that puts everything back. (You'd have to save the plan somewhere first. JSON?)
- Sort `images` further into subfolders by year, using the file's modified time (`p.stat().st_mtime`).

## Docs
- pathlib: https://docs.python.org/3/library/pathlib.html
