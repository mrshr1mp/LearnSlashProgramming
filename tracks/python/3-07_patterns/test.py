from harness import eq


def test_find_dates(sol):
    eq(sol.find_dates("due 2026-03-14, not 2026-13-01"), ["2026-03-14"], "find_dates (month 13 is invalid)")
    eq(sol.find_dates("2025-12-31 to 2026-01-01"), ["2025-12-31", "2026-01-01"], "find_dates with two dates")
    eq(sol.find_dates("2026-02-32 or 2026-00-10"), [], "find_dates with day 32 and month 00")
    eq(sol.find_dates("id 12026-01-015"), [], "find_dates inside a longer number")
    eq(sol.find_dates("nothing here"), [], "find_dates with no dates")


def test_hashtags(sol):
    eq(sol.hashtags("#Python is fun #python #code_daily"), ["python", "code_daily"], "hashtags(...)")
    eq(sol.hashtags("no tags # here"), [], 'hashtags("no tags # here")')
    eq(sol.hashtags("#a1 #B2 #a1!"), ["a1", "b2"], 'hashtags("#a1 #B2 #a1!")')


def test_valid_username(sol):
    for name, want in [("ada_99", True), ("Bob", True), ("ab", False), ("a" * 16, True), ("a" * 17, False),
                       ("9lives", False), ("_ada", False), ("ada lovelace", False), ("ada-99", False), ("", False)]:
        eq(sol.valid_username(name), want, f"valid_username({name!r})")


def test_parse_time_24h(sol):
    for text, want in [("15:07", 907), ("0:00", 0), ("23:59", 1439), ("09:30", 570)]:
        eq(sol.parse_time(text), want, f"parse_time({text!r})")


def test_parse_time_12h(sol):
    for text, want in [("3:07 pm", 907), ("3:07PM", 907), ("12:00 am", 0), ("12:30 pm", 750), ("12:30AM", 30),
                       ("11:59 pm", 1439), ("9:15 Am", 555)]:
        eq(sol.parse_time(text), want, f"parse_time({text!r})")


def test_parse_time_invalid(sol):
    for text in ["25:00", "13:00 pm", "0:30 am", "3:7", "3:075", "noon", "", "12:60"]:
        eq(sol.parse_time(text), None, f"parse_time({text!r})")


def test_redact_numbers(sol):
    eq(sol.redact_numbers("card 1234 5678, pin 12"), "card #### ####, pin 12", "redact_numbers(...)")
    eq(sol.redact_numbers("call 5551234567 now"), "call ########## now", "redact_numbers with a 10-digit number")
    eq(sol.redact_numbers("no numbers"), "no numbers", "redact_numbers with nothing to redact")
