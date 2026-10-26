"""Bank Vault: custom exceptions and context managers."""
from contextlib import contextmanager


class BankError(Exception):
    pass


# TODO: InsufficientFunds and AccountLocked


class Account:
    def __init__(self, owner, balance=0):
        raise NotImplementedError

    def deposit(self, amount):
        raise NotImplementedError

    def withdraw(self, amount):
        raise NotImplementedError


def transfer(src, dst, amount):
    raise NotImplementedError


class Transaction:
    pass


@contextmanager
def frozen(account):
    raise NotImplementedError
    yield
