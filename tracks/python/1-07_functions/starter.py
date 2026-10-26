"""Mission 7: Function Forge."""


def clamp(x, low=0, high=100):
    raise NotImplementedError


def make_greeting(name, greeting="Hello", punctuation="!"):
    raise NotImplementedError


def stats(numbers):
    raise NotImplementedError


def apply_n(func, value, n):
    raise NotImplementedError


def best_by(items, score):
    raise NotImplementedError


if __name__ == "__main__":
    def double(n):
        return n * 2

    print(apply_n(double, 1, 10))
