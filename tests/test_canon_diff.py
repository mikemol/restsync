from restsync.canon import canonicalize
from restsync.diff import diff_values
from restsync.spec import CompareSpec


def test_canonicalize_projects_keys():
    compare = CompareSpec(include=["a", "b"], ignore=["b"])
    value = {"a": 1, "b": 2, "c": 3}
    assert canonicalize(value, compare) == {"a": 1}


def test_diff_values_detects_nested_changes():
    want = {"a": 1, "b": {"c": 2}}
    have = {"a": 1, "b": {"c": 3}}
    assert diff_values(want, have) == {"b": {"c": {"want": 2, "have": 3}}}


def test_diff_values_empty_on_equal():
    want = {"a": 1, "b": [1, 2]}
    have = {"a": 1, "b": [1, 2]}
    assert diff_values(want, have) == {}
