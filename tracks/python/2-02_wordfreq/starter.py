"""wordfreq: find the most common words in a text."""
from pathlib import Path


def words(text):
    """Return all words in text, lowercased. A word = letters a-z and apostrophes."""
    # TODO 1: lowercase the text
    # TODO 2: pull out the words (skip punctuation, numbers, spaces)
    # TODO 3: return them as a list
    raise NotImplementedError


def top_words(text, n=10, ignore=()):
    """Return the n most common words as [(word, count), ...]. Ties go alphabetically."""
    # TODO 1: get the words with words(text), dropping any that are in `ignore`
    # TODO 2: count how often each one appears
    # TODO 3: sort: highest count first, ties alphabetically
    # TODO 4: return the first n
    raise NotImplementedError


if __name__ == "__main__":
    text = (Path(__file__).parent.parent / "samples" / "zen.txt").read_text()
    for word, count in top_words(text, n=10, ignore={"is", "the", "a", "of"}):
        print(f"{count:>3}  {word}")
