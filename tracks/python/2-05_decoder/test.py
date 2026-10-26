from harness import eq

PLAIN_1 = ("Programming is not about typing, it is about thinking. The best programmers "
           "read their error messages carefully and test small pieces of code often.")
PLAIN_2 = ("Every expert was once a beginner who kept going when the code did not work. "
           "Break the problem into tiny steps and solve one step at a time.")


def test_shift_basic(sol):
    eq(sol.shift("Hello, World!", 3), "Khoor, Zruog!", 'shift("Hello, World!", 3)')
    eq(sol.shift("xyz XYZ", 3), "abc ABC", 'shift("xyz XYZ", 3) wraps around')


def test_shift_weird_n(sol):
    eq(sol.shift("abc", -1), "zab", 'shift("abc", -1)')
    eq(sol.shift("abc", 27), "bcd", 'shift("abc", 27)')
    eq(sol.shift("2 + 2 = 4!", 5), "2 + 2 = 4!", "non-letters stay the same")


def test_round_trip(sol):
    eq(sol.shift(sol.shift(PLAIN_1, 11), -11), PLAIN_1, "shift by 11 then -11 gives the original back")


SECRETS = {
    7: "Wyvnyhttpun pz uva hivba afwpun, pa pz hivba aopurpun. Aol ilza wyvnyhttlyz ylhk aolpy lyyvy "
       "tlzzhnlz jhylmbssf huk alza zthss wpljlz vm jvkl vmalu.",
    19: "Xoxkr xqixkm ptl hgvx t uxzbggxk pah dxim zhbgz paxg max vhwx wbw ghm phkd. Ukxtd max ikhuexf "
        "bgmh mbgr lmxil tgw lheox hgx lmxi tm t mbfx.",
    0: PLAIN_1,
    25: "Dudqx dwodqs vzr nmbd z adfhmmdq vgn jdos fnhmf vgdm sgd bncd chc mns vnqj. Aqdzj sgd oqnakdl "
        "hmsn shmx rsdor zmc rnkud nmd rsdo zs z shld.",
}


def test_crack(sol):
    for key, secret in SECRETS.items():
        eq(sol.crack(secret), key, f"crack() on a message shifted by {key}")
