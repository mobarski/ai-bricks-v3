import pytest

import aibricks


def test_client_basic():
    client = aibricks.client()
    resp = client.chat.completions.create(
        model='openrouter:meta-llama/llama-3.2-1b-instruct:free',
        messages=[{"role": "user", "content": "Tell me a joke."}],
        temperature=0.7)
    try:
        content = resp.choices[0].message.content
    except KeyError as e:
        print(resp)
        raise e
    assert content


def test_client_model():
    client = aibricks.client(
        model='openrouter:meta-llama/llama-3.2-1b-instruct:free',
        temperature=0.7)
    resp = client.chat.completions.create(
        model='xxx',
        messages=[{"role": "user", "content": "Tell me a joke."}],)
    try:
        content = resp.choices[0].message.content
    except KeyError as e:
        print(resp)
        raise e
    assert content


def test_client_model_lambda():
    client = aibricks.client(
        model=lambda x: 'openrouter:meta-llama/llama-3.2-1b-instruct:free',
        temperature=0.0,
        max_tokens=1,
        )
    resp = client.chat.completions.create(
        model='xxx',
        messages=[{"role": "user", "content": "Tell me a joke."}],
        max_tokens=20,
        )
    try:
        content = resp.choices[0].message.content
        print(content)
        print(resp)
    except KeyError as e:
        print(resp)
        raise e
    assert content


@pytest.mark.parametrize("conn_id", [
    'connections.default',
    'connections.aux',
])
def test_client_from_config(conn_id):
    cfg = aibricks.load_config('tests/aibricks/test_data/config/connections.yaml')
    client = aibricks.client(from_config=conn_id, config=cfg) # FIXME: kwargs are not passed to connect
    resp = client.chat.completions.create(None, messages=[{"role": "user", "content": "Tell me a joke."}])
    try:
        content = resp.choices[0].message.content
        print(content)
    except KeyError as e:
        print(resp)
        raise e
    assert content
