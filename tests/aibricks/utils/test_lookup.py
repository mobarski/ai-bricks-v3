import pytest
from aibricks.utils import lookup
from aibricks.namespace import DictNamespace


def test_lookup_basic_dict():
    data = {'a': {'b': 'c'}}
    assert lookup(data, 'a.b') == 'c'


def test_lookup_list():
    data = {'items': [{'name': 'first'}, {'name': 'second'}]}
    assert lookup(data, 'items.0.name') == 'first'
    assert lookup(data, 'items.1.name') == 'second'


def test_lookup_negative_indices():
    data = {'items': [{'name': 'first'}, {'name': 'second'}, {'name': 'third'}]}
    assert lookup(data, 'items.-1.name') == 'third'
    assert lookup(data, 'items.-2.name') == 'second'
    assert lookup(data, 'items.-3.name') == 'first'


def test_lookup_negative_indices_out_of_range():
    data = {'items': [{'name': 'first'}, {'name': 'second'}]}
    with pytest.raises(KeyError):
        lookup(data, 'items.-3.name')


def test_lookup_with_default():
    data = {'a': 1}
    assert lookup(data, 'b', default='not found') == 'not found'


def test_lookup_missing_no_default():
    data = {'a': 1}
    with pytest.raises(KeyError):
        lookup(data, 'b')


def test_lookup_object_attributes():
    class TestObj:
        def __init__(self):
            self.value = 'test'

    data = {'obj': TestObj()}
    assert lookup(data, 'obj.value') == 'test'


def test_lookup_namespace():
    ns = DictNamespace({'user': {'name': 'John'}})
    assert lookup(ns._data, 'user.name') == 'John'


def test_lookup_empty():
    assert lookup({}, 'any.path', default=None) is None


def test_lookup_nested_complex():
    data = {
        'users': [
            {'profile': {'name': 'Alice', 'settings': {'theme': 'dark'}}},
            {'profile': {'name': 'Bob', 'settings': {'theme': 'light'}}}
        ]
    }
    assert lookup(data, 'users.0.profile.settings.theme') == 'dark'
    assert lookup(data, 'users.1.profile.name') == 'Bob'
    assert lookup(data, 'users.-1.profile.name') == 'Bob'
    assert lookup(data, 'users.-2.profile.settings.theme') == 'dark'
