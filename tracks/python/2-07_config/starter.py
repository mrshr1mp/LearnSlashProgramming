"""config: deep-merge settings and read them with dotted paths."""


def merge(base, override):
    raise NotImplementedError


def get(config, path, default=None):
    raise NotImplementedError


def flatten(config):
    raise NotImplementedError
