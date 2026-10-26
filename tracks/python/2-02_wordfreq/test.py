from harness import eq

TEXT = "The cat and the hat. THE END, and that's that!"


def test_words(sol):
    eq(sol.words("Don't PANIC, ok?"), ["don't", "panic", "ok"], 'words("Don\'t PANIC, ok?")')
    eq(sol.words("  42 apples...and 7 pears "), ["apples", "and", "pears"], "words skips numbers and punctuation")
    eq(sol.words(""), [], 'words("")')


def test_top_words(sol):
    eq(sol.top_words(TEXT, n=3), [("the", 3), ("and", 2), ("cat", 1)], "top_words(TEXT, n=3)")


def test_ties_alphabetical(sol):
    want = [("the", 3), ("and", 2), ("cat", 1), ("end", 1), ("hat", 1), ("that", 1), ("that's", 1)]
    eq(sol.top_words(TEXT), want, "top_words(TEXT): ties must be alphabetical")


def test_ignore(sol):
    eq(sol.top_words(TEXT, n=2, ignore={"the", "and"}), [("cat", 1), ("end", 1)], "top_words with ignore={'the', 'and'}")


def test_empty(sol):
    eq(sol.top_words(""), [], 'top_words("")')
