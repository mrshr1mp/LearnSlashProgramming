from harness import eq

HALL = "A dusty hall with a flickering torch. You see: lamp. Exits: east, north."
HALL_EMPTY = "A dusty hall with a flickering torch. Exits: east, north."
LIBRARY = "Tall shelves of crumbling books. You see: key, book. Exits: south."
KITCHEN = "It smells like very old soup. Exits: down, west."
CELLAR = "A cold cellar. A heavy chest sits in the corner. Exits: up."
WIN = "The key turns. Inside the chest: a golden snake. You win!"


def play(sol, *commands):
    state = sol.new_game()
    return state, [sol.do(state, c) for c in commands]


def test_new_game(sol):
    state = sol.new_game()
    eq(state["room"], "hall", 'new_game()["room"]')
    eq(state["inventory"], [], 'new_game()["inventory"]')
    eq(state["won"], False, 'new_game()["won"]')


def test_look(sol):
    _, out = play(sol, "look")
    eq(out[0], HALL, '"look" in the hall')


def test_go(sol):
    state, out = play(sol, "go north", "go south", "go east", "go up", "go")
    eq(out, [LIBRARY, HALL, KITCHEN, "You can't go that way.", "Go where?"],
       'messages for: "go north", "go south", "go east", "go up", "go"')
    eq(state["room"], "kitchen", "room after those moves")


def test_messy_commands(sol):
    _, out = play(sol, "  GO   North ", "LOOK", "dance")
    eq(out, [LIBRARY, LIBRARY, "I don't understand that."], 'messages for: "  GO   North ", "LOOK", "dance"')


def test_take_and_inventory(sol):
    state, out = play(sol, "inventory", "take lamp", "take lamp", "take", "look", "go north", "take book",
                      "take key", "inventory")
    eq(out, ["You carry nothing.", "Taken: lamp.", "There is no lamp here.", "Take what?", HALL_EMPTY, LIBRARY,
             "Taken: book.", "Taken: key.", "You carry: lamp, book, key."],
       "messages for a take/inventory sequence")
    eq(state["inventory"], ["lamp", "book", "key"], 'state["inventory"]')


def test_dark_cellar(sol):
    state, out = play(sol, "go east", "go down")
    eq(out[1], "It's too dark to go down there without a light.", '"go down" without the lamp')
    eq(state["room"], "kitchen", "room after trying the dark cellar")


def test_games_are_separate(sol):
    play(sol, "take lamp")
    _, out = play(sol, "look")
    eq(out[0], HALL, '"look" in a NEW game after taking the lamp in an old game')


def test_win(sol):
    state, out = play(sol, "open chest", "take lamp", "go east", "go down", "open chest", "go up", "go west",
                      "go north", "take key", "go south", "go east", "go down", "open chest")
    eq(out[0], "There is nothing to open here.", '"open chest" in the hall')
    eq(out[3], CELLAR, "entering the cellar with the lamp")
    eq(out[4], "The chest is locked.", '"open chest" without the key')
    eq(out[-1], WIN, '"open chest" with the key')
    eq(state["won"], True, 'state["won"] after winning')
