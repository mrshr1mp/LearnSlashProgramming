import dataclasses

from harness import eq, raises


def pancakes(sol):
    I, U = sol.Ingredient, sol.Unit
    return sol.Recipe("pancakes", 2, [I("flour", 200, U.GRAM), I("milk", 300, U.ML), I("egg", 2, U.PIECE)])


def test_unit(sol):
    eq([u.value for u in sol.Unit], ["g", "ml", "pc"], "the Unit values")
    eq(sol.Unit("ml"), sol.Unit.ML, 'Unit("ml")')


def test_ingredient(sol):
    I = sol.Ingredient
    assert dataclasses.is_dataclass(I), "Ingredient should be a dataclass"
    egg = I("egg", 2, sol.Unit.PIECE)
    eq(egg, I("egg", 2, sol.Unit.PIECE), "two equal Ingredients")
    raises(AttributeError, setattr, egg, "amount", 5)
    raises(ValueError, I, "salt", 0, sol.Unit.GRAM)
    raises(ValueError, I, "salt", -1, sol.Unit.GRAM)


def test_recipe_default_list(sol):
    a, b = sol.Recipe("a", 1), sol.Recipe("b", 1)
    a.ingredients.append(sol.Ingredient("x", 1, sol.Unit.GRAM))
    eq(b.ingredients, [], "a second Recipe's ingredients after appending to the first (they must not share a list)")


def test_scale(sol):
    p = pancakes(sol)
    big = p.scale(3)
    eq([(i.name, i.amount) for i in big.ingredients], [("flour", 300.0), ("milk", 450.0), ("egg", 3.0)],
       "ingredients of pancakes.scale(3)")
    eq(big.servings, 3, "servings after scale(3)")
    eq(p.ingredients[0].amount, 200, "the original recipe after scaling (must not change)")
    eq(p.scale(3 / 7 * 2).ingredients[0].amount, 85.71, "amounts are rounded to 2 decimals")


def test_json_round_trip(sol):
    p = pancakes(sol)
    text = p.to_json()
    assert isinstance(text, str), "to_json() should return a string"
    eq(sol.Recipe.from_json(text), p, "Recipe.from_json(recipe.to_json())")


def test_shopping_list(sol):
    I, U = sol.Ingredient, sol.Unit
    omelette = sol.Recipe("omelette", 1, [I("egg", 3, U.PIECE), I("milk", 50, U.ML)])
    eq(sol.shopping_list(pancakes(sol), omelette),
       {"flour": (200, U.GRAM), "milk": (350, U.ML), "egg": (5, U.PIECE)}, "shopping_list(pancakes, omelette)")
    weird = sol.Recipe("weird", 1, [I("milk", 1, U.GRAM)])
    raises(ValueError, sol.shopping_list, pancakes(sol), weird)
