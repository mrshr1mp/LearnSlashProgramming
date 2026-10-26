"""One-Liners: every function works. Make each body a single return statement."""


def squares_of_evens(nums):
    result = []
    for n in nums:
        if n % 2 == 0:
            result.append(n * n)
    return result


def word_lengths(words):
    result = {}
    for w in words:
        result[w] = len(w)
    return result


def first_letters(names):
    """Set of uppercase first letters of the non-empty names."""
    result = set()
    for name in names:
        if name:
            result.add(name[0].upper())
    return result


def numbered(items):
    result = []
    i = 1
    for item in items:
        result.append(str(i) + ". " + item)
        i += 1
    return result


def all_positive(nums):
    for n in nums:
        if n <= 0:
            return False
    return True


def has_duplicates(items):
    seen = []
    for item in items:
        if item in seen:
            return True
        seen.append(item)
    return False


def transpose(matrix):
    result = []
    for col in range(len(matrix[0]) if matrix else 0):
        row = []
        for r in matrix:
            row.append(r[col])
        result.append(row)
    return result


def flatten(lists):
    result = []
    for sub in lists:
        for x in sub:
            result.append(x)
    return result


def total_price(cart):
    total = 0
    for item in cart:
        total += item["price"] * item["qty"]
    return total
