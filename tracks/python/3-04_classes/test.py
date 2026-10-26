from harness import eq, raises


def test_vector_basics(sol):
    v = sol.Vector(1, 2)
    eq((v.x, v.y), (1, 2), "Vector(1, 2).x and .y")
    eq(repr(v), "Vector(1, 2)", "repr(Vector(1, 2))")


def test_vector_math(sol):
    V = sol.Vector
    eq(V(1, 2) + V(3, 4), V(4, 6), "Vector(1, 2) + Vector(3, 4)")
    eq(V(5, 5) - V(1, 2), V(4, 3), "Vector(5, 5) - Vector(1, 2)")
    eq(V(1, 2) * 3, V(3, 6), "Vector(1, 2) * 3")
    eq(3 * V(1, 2), V(3, 6), "3 * Vector(1, 2)")
    eq(abs(V(3, 4)), 5.0, "abs(Vector(3, 4))")


def test_vector_equality_and_hash(sol):
    V = sol.Vector
    eq(V(1, 2) == V(1, 2), True, "Vector(1, 2) == Vector(1, 2)")
    eq(V(1, 2) == V(2, 1), False, "Vector(1, 2) == Vector(2, 1)")
    eq(V(1, 2) == (1, 2), False, "Vector(1, 2) == (1, 2) (a tuple is not a Vector)")
    eq(len({V(1, 2), V(1, 2), V(0, 0)}), 2, "size of a set of 3 vectors where 2 are equal")


def test_shape_base(sol):
    raises(NotImplementedError, sol.Shape().area)


def test_areas(sol):
    eq(round(sol.Circle(1).area(), 5), 3.14159, "Circle(1).area() (rounded)")
    eq(sol.Rect(2, 3).area(), 6, "Rect(2, 3).area()")
    eq(sol.Square(3).area(), 9, "Square(3).area()")


def test_inheritance(sol):
    sq = sol.Square(3)
    assert isinstance(sq, sol.Rect), "Square should inherit from Rect"
    assert isinstance(sq, sol.Shape), "Square should be a Shape"
    eq((sq.width, sq.height), (3, 3), "Square(3).width and .height")


def test_perimeter_property(sol):
    eq(sol.Rect(2, 3).perimeter, 10, "Rect(2, 3).perimeter (a property, so no parentheses)")
    eq(sol.Square(4).perimeter, 16, "Square(4).perimeter")


def test_describe(sol):
    eq(sol.Circle(1).describe(), "Circle with area 3.14", "Circle(1).describe()")
    eq(sol.Square(2).describe(), "Square with area 4.00", "Square(2).describe()")


def test_sorting(sol):
    shapes = [sol.Square(3), sol.Circle(1), sol.Rect(1, 2)]
    eq([type(s).__name__ for s in sorted(shapes)], ["Rect", "Circle", "Square"], "sorted(shapes) by area")
