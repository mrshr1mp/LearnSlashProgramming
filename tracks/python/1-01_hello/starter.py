"""Mission 1: Hello, Python. Run this file with the play button to try your functions."""


def greet(name):
    # This one is done for you, as an example.
    return f"Hello, {name}!"


def shout(text):
    # "hey there" -> "HEY THERE!"
    raise NotImplementedError


def introduce(name, age):
    # ("Ada", 36) -> "Hi, I'm Ada and I'm 36 years old."
    raise NotImplementedError


def initials(full_name):
    # "ada lovelace" -> "A.L."
    raise NotImplementedError


# This part only runs when you run this file yourself (not when the checker runs).
if __name__ == "__main__":
    print(greet("World"))
    print(shout("it works"))
