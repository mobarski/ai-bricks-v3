import aibricks


def test_client_basic():
    client = aibricks.client()
    resp = client.chat.completions.create(
        model='openrouter:meta-llama/llama-3.2-1b-instruct:free',
        messages=[{"role": "user", "content": "Tell me a joke."}],
        temperature=0.7)
    try:
        content = resp['choices'][0]['message']['content']
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
        content = resp['choices'][0]['message']['content']
    except KeyError as e:
        print(resp)
        raise e
    assert content


def test_client_model_lambda():
    client = aibricks.client(
        model=lambda x: 'openrouter:meta-llama/llama-3.2-1b-instruct:free',
        temperature=0.7)
    resp = client.chat.completions.create(
        model='xxx',
        messages=[{"role": "user", "content": "Tell me a joke."}],)
    try:
        content = resp['choices'][0]['message']['content']
    except KeyError as e:
        print(resp)
        raise e
    assert content
