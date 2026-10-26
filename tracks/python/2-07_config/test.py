import copy

from harness import eq


def configs():
    base = {"db": {"host": "localhost", "port": 5432, "pool": {"min": 1, "max": 5}},
            "log": {"level": "info"}, "debug": False, "tags": ["a"]}
    override = {"db": {"port": 6543, "pool": {"max": 20}}, "debug": True, "tags": ["b"]}
    return base, override


MERGED = {"db": {"host": "localhost", "port": 6543, "pool": {"min": 1, "max": 20}},
          "log": {"level": "info"}, "debug": True, "tags": ["b"]}


def test_merge(sol):
    eq(sol.merge(*configs()), MERGED, "merge(base, override)")


def test_merge_type_changes(sol):
    eq(sol.merge({"a": {"b": 1}}, {"a": 5}), {"a": 5}, "override replaces a dict with a number")
    eq(sol.merge({"a": 5}, {"a": {"b": 1}}), {"a": {"b": 1}}, "override replaces a number with a dict")
    eq(sol.merge({}, {"x": 1}), {"x": 1}, "merge into empty dict")


def test_merge_no_side_effects(sol):
    base, override = configs()
    before = copy.deepcopy((base, override))
    result = sol.merge(base, override)
    eq((base, override), before, "base and override after merge (they must not change)")
    result["db"]["pool"]["min"] = 99
    result["log"]["level"] = "debug"
    result["tags"].append("z")
    eq(base, before[0], "base after editing the merge result (is a nested dict shared?)")
    eq(override, before[1], "override after editing the merge result (is a list shared?)")


def test_get(sol):
    cfg = MERGED
    eq(sol.get(cfg, "db.port"), 6543, 'get(cfg, "db.port")')
    eq(sol.get(cfg, "db.pool.max"), 20, 'get(cfg, "db.pool.max")')
    eq(sol.get(cfg, "debug"), True, 'get(cfg, "debug")')
    eq(sol.get(cfg, "db.nope", "fallback"), "fallback", 'get(cfg, "db.nope", "fallback")')
    eq(sol.get(cfg, "debug.deeper"), None, 'get(cfg, "debug.deeper") where debug is not a dict')


def test_flatten(sol):
    want = {"db.host": "localhost", "db.port": 6543, "db.pool.min": 1, "db.pool.max": 20,
            "log.level": "info", "debug": True, "tags": ["b"]}
    eq(sol.flatten(MERGED), want, "flatten(merged config)")
