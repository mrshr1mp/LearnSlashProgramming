"""Runs a mission's test.py against your code. Usage: harness.py TEST SOLUTION

A test file is plain Python: every function named test_* gets your module
(or just the file path, if the test sets PATH_ONLY = True).
"""
import importlib.util
import sys
import traceback
from pathlib import Path


def eq(got, want, what):
    assert got == want, f"{what}\n          got:      {got!r}\n          expected: {want!r}"


def raises(exc, fn, *args, **kwargs):
    call = f"{fn.__name__}{args}"
    try:
        fn(*args, **kwargs)
    except exc:
        return
    except Exception as e:
        raise AssertionError(f"{call} should raise {exc.__name__}, but raised {type(e).__name__}: {e}")
    raise AssertionError(f"{call} should raise {exc.__name__}, but it didn't")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def show_error(e):
    # hide the harness's and importlib's own frames: only the test and the learner's code matter
    te = traceback.TracebackException.from_exception(e)
    te.stack = traceback.StackSummary.from_list(
        [f for f in te.stack if Path(f.filename).name != "harness.py" and not f.filename.startswith("<frozen")])
    print("".join(te.format()), end="")


def main(test_path, solution_path):
    tests = load("mission_test", test_path)
    if getattr(tests, "PATH_ONLY", False):
        target = solution_path
    else:
        try:
            target = load("your_file", solution_path)
        except Exception as e:
            print("  Your file crashed before any test could run:\n")
            show_error(e)
            return 1
    failed = 0
    for name, fn in vars(tests).items():
        if not name.startswith("test_"):
            continue
        try:
            fn(target)
            print(f"  PASS   {name}")
        except NotImplementedError:
            failed += 1
            print(f"  TODO   {name}: you haven't written this part yet")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL   {name}: {e}")
        except Exception as e:
            failed += 1
            print(f"  CRASH  {name}: your code raised an error. Read it bottom-up:\n")
            show_error(e)
            print()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
