"""Mission 8 BOSS: a text adventure engine. Read the brief for the exact rules."""

WORLD = {
    "hall": {
        "desc": "A dusty hall with a flickering torch.",
        "exits": {"north": "library", "east": "kitchen"},
        "items": ["lamp"],
    },
    "library": {
        "desc": "Tall shelves of crumbling books.",
        "exits": {"south": "hall"},
        "items": ["key", "book"],
    },
    "kitchen": {
        "desc": "It smells like very old soup.",
        "exits": {"west": "hall", "down": "cellar"},
        "items": [],
    },
    "cellar": {
        "desc": "A cold cellar. A heavy chest sits in the corner.",
        "exits": {"up": "kitchen"},
        "items": [],
    },
}


def new_game():
    raise NotImplementedError


def do(state, command):
    raise NotImplementedError


# Run this file to play your game!
if __name__ == "__main__":
    state = new_game()
    print(do(state, "look"))
    while not state["won"]:
        command = input("> ")
        if command == "quit":
            break
        print(do(state, command))
