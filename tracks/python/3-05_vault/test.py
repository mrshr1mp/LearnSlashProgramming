from harness import eq, raises


def test_exception_family(sol):
    assert issubclass(sol.InsufficientFunds, sol.BankError), "InsufficientFunds should inherit from BankError"
    assert issubclass(sol.AccountLocked, sol.BankError), "AccountLocked should inherit from BankError"
    assert issubclass(sol.BankError, Exception), "BankError should inherit from Exception"


def test_deposit_withdraw(sol):
    a = sol.Account("ada", 50)
    eq((a.owner, a.balance, a.locked), ("ada", 50, False), "a new Account('ada', 50)")
    a.deposit(25)
    a.withdraw(10)
    eq(a.balance, 65, "balance after deposit(25) and withdraw(10)")
    eq(sol.Account("bob").balance, 0, "default balance")


def test_bad_amounts(sol):
    a = sol.Account("ada", 50)
    raises(ValueError, a.deposit, 0)
    raises(ValueError, a.withdraw, -5)
    eq(a.balance, 50, "balance after rejected amounts")


def test_insufficient_funds(sol):
    a = sol.Account("ada", 30)
    try:
        a.withdraw(100)
    except sol.InsufficientFunds as e:
        eq(e.needed, 70, "InsufficientFunds.needed when withdrawing 100 from 30")
    else:
        raise AssertionError("withdraw(100) from a balance of 30 should raise InsufficientFunds")
    eq(a.balance, 30, "balance after a failed withdraw")


def test_locked(sol):
    a = sol.Account("ada", 30)
    a.locked = True
    raises(sol.AccountLocked, a.deposit, 5)
    raises(sol.AccountLocked, a.withdraw, 5)
    eq(a.balance, 30, "balance of a locked account")


def test_transfer(sol):
    a, b = sol.Account("a", 100), sol.Account("b", 0)
    sol.transfer(a, b, 40)
    eq((a.balance, b.balance), (60, 40), "balances after transfer(a, b, 40)")


def test_transfer_is_all_or_nothing(sol):
    a, b = sol.Account("a", 100), sol.Account("b", 0)
    raises(sol.InsufficientFunds, sol.transfer, a, b, 500)
    eq((a.balance, b.balance), (100, 0), "balances after a transfer that's too big")
    b.locked = True
    raises(sol.AccountLocked, sol.transfer, a, b, 40)
    eq((a.balance, b.balance), (100, 0), "balances after a transfer INTO a locked account (no money may vanish)")


def test_transaction(sol):
    a = sol.Account("a", 100)
    with sol.Transaction(a):
        a.withdraw(30)
    eq(a.balance, 70, "balance after a successful Transaction block")
    try:
        with sol.Transaction(a):
            a.withdraw(50)
            raise RuntimeError("power cut")
    except RuntimeError:
        pass
    else:
        raise AssertionError("the RuntimeError should come out of the with-block (don't swallow it)")
    eq(a.balance, 70, "balance after a Transaction block that crashed (should be rolled back)")


def test_frozen(sol):
    a = sol.Account("a", 100)
    with sol.frozen(a):
        eq(a.locked, True, ".locked inside frozen()")
        raises(sol.AccountLocked, a.withdraw, 1)
    eq(a.locked, False, ".locked after frozen()")
    try:
        with sol.frozen(a):
            raise KeyError("oops")
    except KeyError:
        pass
    eq(a.locked, False, ".locked after a frozen() block that crashed")
    a.locked = True
    with sol.frozen(a):
        pass
    eq(a.locked, True, ".locked after frozen() on an already-locked account (put it back how it was)")
