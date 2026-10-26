"""Infinite Streams: iterators and generators."""
from collections import deque
from itertools import count, islice, takewhile


class Countdown:
    def __init__(self, start):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError


def fibonacci():
    raise NotImplementedError


def primes():
    raise NotImplementedError


def take(n, iterable):
    raise NotImplementedError


def window(iterable, size):
    raise NotImplementedError


def chunked(iterable, n):
    raise NotImplementedError
