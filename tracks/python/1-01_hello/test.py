from harness import eq


def test_greet(sol):
    eq(sol.greet("Ada"), "Hello, Ada!", 'greet("Ada")')


def test_shout(sol):
    eq(sol.shout("hey there"), "HEY THERE!", 'shout("hey there")')
    eq(sol.shout("Python"), "PYTHON!", 'shout("Python")')


def test_introduce(sol):
    eq(sol.introduce("Ada", 36), "Hi, I'm Ada and I'm 36 years old.", 'introduce("Ada", 36)')
    eq(sol.introduce("Linus", 19), "Hi, I'm Linus and I'm 19 years old.", 'introduce("Linus", 19)')


def test_initials(sol):
    eq(sol.initials("ada lovelace"), "A.L.", 'initials("ada lovelace")')
    eq(sol.initials("Alan Turing"), "A.T.", 'initials("Alan Turing")')
