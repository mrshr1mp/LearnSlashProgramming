"""Shape Arena: dunder methods, inheritance, properties."""
import math


class Vector:
    def __init__(self, x, y):
        raise NotImplementedError


class Shape:
    def area(self):
        raise NotImplementedError

    def describe(self):
        raise NotImplementedError


class Circle(Shape):
    pass


class Rect(Shape):
    pass


class Square(Rect):
    pass
