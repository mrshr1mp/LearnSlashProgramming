"""Bug Bounty: your tests for textkit. Each test gets `m`, the module being tested."""


def test_slugify_simple(m):
    assert m.slugify("Hello World") == "hello-world"


# Write more tests below. Catch all 8 hidden bugs!


# Run this file to try your tests on the real textkit (in ../samples).
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent / "samples"))
    import textkit

    for name, test in list(globals().items()):
        if name.startswith("test_"):
            try:
                test(textkit)
                print("PASS", name)
            except Exception as e:
                print("FAIL", name, repr(e))
