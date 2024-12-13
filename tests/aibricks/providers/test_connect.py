import pytest

import aibricks


@pytest.mark.parametrize("model_id", [
    "openai:gpt-4o-mini",
    "openrouter:meta-llama/llama-3.2-1b-instruct:free",
    "google:gemini-1.5-flash-8b",
    "xai:grok-beta",
    "together:meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
    "arliai:Mistral-Nemo-12B-Instruct-2407",
])
def test_online_provider(model_id):
    conn = aibricks.connect(model_id)
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    try:
        content = resp['choices'][0]['message']['content']
        print(content)
    except KeyError as e:
        print(resp)
        raise e
    assert content


@pytest.mark.parametrize("conn_id", [
    'connections.default',
    'connections.aux',
])
def test_connect_from_config(conn_id):
    cfg = aibricks.load_config('tests/aibricks/test_data/config/connections.yaml')
    conn = aibricks.connect(from_config=conn_id, config=cfg)
    return
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    try:
        content = resp['choices'][0]['message']['content']
        print(content)
    except KeyError as e:
        print(resp)
        raise e
    assert content
