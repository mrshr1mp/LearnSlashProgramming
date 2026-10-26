from harness import eq


def test_letter_counts(sol):
    eq(sol.letter_counts("Hello!"), {"h": 1, "e": 1, "l": 2, "o": 1}, 'letter_counts("Hello!")')
    eq(sol.letter_counts("A a, 1 2"), {"a": 2}, 'letter_counts("A a, 1 2")')
    eq(sol.letter_counts(""), {}, 'letter_counts("")')


def test_invert(sol):
    eq(sol.invert({"a": 1, "b": 2}), {1: "a", 2: "b"}, 'invert({"a": 1, "b": 2})')
    eq(sol.invert({}), {}, "invert({})")


def test_group_by_length(sol):
    eq(sol.group_by_length(["cat", "horse", "dog"]), {3: ["cat", "dog"], 5: ["horse"]},
       'group_by_length(["cat", "horse", "dog"])')
    eq(sol.group_by_length([]), {}, "group_by_length([])")


def test_restock(sol):
    inv, delivery = {"apples": 5, "pears": 2}, {"apples": 10, "kiwis": 4}
    eq(sol.restock(inv, delivery), {"apples": 15, "pears": 2, "kiwis": 4}, "restock(...)")
    eq(inv, {"apples": 5, "pears": 2}, "the inventory dict after restock (it must not change!)")
    eq(delivery, {"apples": 10, "kiwis": 4}, "the delivery dict after restock (it must not change!)")
