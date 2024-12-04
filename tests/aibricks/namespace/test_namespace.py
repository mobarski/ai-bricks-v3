import pytest
from aibricks.namespace import DictNamespace


def test_basic_dict_access():
    data = {'a': 1, 'b': 2}
    ns = DictNamespace(data)
    assert ns.a == 1
    assert ns['a'] == 1
    assert ns.b == 2
    assert ns['b'] == 2


def test_nested_dict_access():
    data = {'user': {'name': 'John', 'age': 30}}
    ns = DictNamespace(data)
    assert ns.user.name == 'John'
    assert ns['user']['name'] == 'John'
    assert ns.lookup('user.name') == 'John'


def test_list_access():
    data = {'items': [{'id': 1}, {'id': 2}]}
    ns = DictNamespace(data)
    assert ns.items[0]['id'] == 1
    assert ns.items[1]['id'] == 2


def test_mixed_access():
    data = {
        'users': [
            {'name': 'John', 'contacts': {'email': 'john@example.com'}},
            {'name': 'Jane', 'contacts': {'email': 'jane@example.com'}}
        ]
    }
    ns = DictNamespace(data)
    assert ns.users[0].name == 'John'
    assert ns.users[0].contacts.email == 'john@example.com'
    assert ns.lookup('users.0.contacts.email') == 'john@example.com'


def test_lookup_with_default():
    data = {'a': {'b': {'c': 1}}}
    ns = DictNamespace(data)
    assert ns.lookup('a.b.c') == 1
    assert ns.lookup('a.b.d', default='not found') == 'not found'
    assert ns.lookup('x.y.z', default=None) is None


def test_attribute_error():
    ns = DictNamespace({'a': 1})
    with pytest.raises(AttributeError):
        _ = ns.nonexistent


def test_key_error():
    ns = DictNamespace({'a': 1})
    with pytest.raises(KeyError):
        _ = ns['nonexistent']


def test_lookup_with_exceptions():
    data = {
        'a': {
            'b': {
                'c': 'value',
                'list': [
                    {'item': 1},
                    {'item': 2}
                ]
            }
        }
    }
    ns = DictNamespace(data)

    # Test successful lookups
    assert ns.lookup('a.b.c') == 'value'
    assert ns.lookup('a.b.list.0.item') == 1

    # Test with default value
    assert ns.lookup('a.b.missing', 'default') == 'default'
    assert ns.lookup('a.b.list.99', 'default') == 'default'

    # Test with Ellipsis (...)
    with pytest.raises(KeyError):
        ns.lookup('a.b.missing', ...)

    with pytest.raises(KeyError):
        ns.lookup('a.b.list.99', ...)

    # Test that default=None works as expected
    assert ns.lookup('a.b.missing', None) is None
    assert ns.lookup('a.b.list.99', None) is None
