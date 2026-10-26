from harness import eq


def test_countdown(sol):
    eq(sol.countdown(3), [3, 2, 1, "Liftoff!"], "countdown(3)")
    eq(sol.countdown(0), ["Liftoff!"], "countdown(0)")


def test_top3(sol):
    scores = [50, 90, 70, 85]
    eq(sol.top3(scores), [90, 85, 70], "top3([50, 90, 70, 85])")
    eq(scores, [50, 90, 70, 85], "the scores list after calling top3 (it must not change!)")
    eq(sol.top3([4, 9]), [9, 4], "top3([4, 9])")


def test_unique(sol):
    eq(sol.unique([3, 1, 3, 2, 1]), [3, 1, 2], "unique([3, 1, 3, 2, 1])")
    eq(sol.unique(["a", "b", "a"]), ["a", "b"], 'unique(["a", "b", "a"])')
    eq(sol.unique([]), [], "unique([])")


def test_chunk(sol):
    eq(sol.chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]], "chunk([1, 2, 3, 4, 5], 2)")
    eq(sol.chunk([1, 2, 3], 3), [[1, 2, 3]], "chunk([1, 2, 3], 3)")
    eq(sol.chunk([], 4), [], "chunk([], 4)")


def test_rotate(sol):
    eq(sol.rotate([1, 2, 3, 4], 1), [4, 1, 2, 3], "rotate([1, 2, 3, 4], 1)")
    eq(sol.rotate([1, 2, 3, 4], 2), [3, 4, 1, 2], "rotate([1, 2, 3, 4], 2)")
    eq(sol.rotate([1, 2, 3, 4], 5), [4, 1, 2, 3], "rotate([1, 2, 3, 4], 5)")
    eq(sol.rotate([1, 2, 3], 0), [1, 2, 3], "rotate([1, 2, 3], 0)")
    eq(sol.rotate([], 3), [], "rotate([], 3)")
