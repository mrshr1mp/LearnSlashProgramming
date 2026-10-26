from harness import eq

MAP = """
##..#
#...#
..#..
.....
##.##
"""


def test_parse(sol):
    eq(sol.parse(MAP), ["##..#", "#...#", "..#..", ".....", "##.##"], "parse(MAP)")
    eq(sol.parse("#.  \n\n.#\n"), ["#.", ".#"], "parse with trailing spaces and blank lines")


def test_islands(sol):
    eq(sol.islands(sol.parse(MAP)), [3, 2, 2, 2, 1], "islands on the example map")


def test_diagonal_not_connected(sol):
    eq(sol.islands(["#.", ".#"]), [1, 1], "diagonal cells are separate islands")


def test_no_land(sol):
    eq(sol.islands(["...", "..."]), [], "islands on all water")


def test_ring_with_lake(sol):
    ring = ["#####", "#...#", "#.#.#", "#...#", "#####"]
    eq(sol.islands(ring), [16, 1], "a ring of land with a tiny island in the lake")


def test_huge_island(sol):
    eq(sol.islands(["#" * 300] * 300), [90000], "300x300 solid land")
