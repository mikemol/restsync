from restsync.canon import canonicalize
from restsync.diff import diff_values
from restsync.spec import CompareSpec


def test_canonicalize_projects_keys():
    compare = CompareSpec(include=["a", "b"], ignore=["b"])
    value = {"a": 1, "b": 2, "c": 3}
    assert canonicalize(value, compare) == {"a": 1}


def test_canonicalize_keeps_nested_keys():
    compare = CompareSpec(include=["parent"])
    value = {"parent": {"child": 1, "child2": 2}}
    assert canonicalize(value, compare) == {"parent": {"child": 1, "child2": 2}}


def test_canonicalize_ignores_nested_keys():
    compare = CompareSpec(include=["parent"], ignore=["skip"])
    value = {"parent": {"skip": 1, "keep": 2}}
    assert canonicalize(value, compare) == {"parent": {"keep": 2}}


def test_canonicalize_unwraps_enabled_fields():
    compare = CompareSpec(include=["toggle", "other"], unwrap_enabled=["toggle"])
    value = {"toggle": {"enabled": False}, "other": {"enabled": True}}
    assert canonicalize(value, compare) == {"toggle": False, "other": {"enabled": True}}


def test_diff_values_detects_nested_changes():
    want = {"a": 1, "b": {"c": 2}}
    have = {"a": 1, "b": {"c": 3}}
    assert diff_values(want, have) == {"b": {"c": {"want": 2, "have": 3}}}


def test_diff_values_empty_on_equal():
    want = {"a": 1, "b": [1, 2]}
    have = {"a": 1, "b": [1, 2]}
    assert diff_values(want, have) == {}
