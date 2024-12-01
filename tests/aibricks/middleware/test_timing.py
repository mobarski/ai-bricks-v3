from types import SimpleNamespace

import pytest

import aibricks
from aibricks.middleware import TimingMiddleware


@pytest.mark.parametrize("model_id", [
    "openai:gpt-4o-mini",
    "openrouter:meta-llama/llama-3.2-1b-instruct:free",
    "google:gemini-1.5-flash-8b",
    "arliai:Mistral-Nemo-12B-Instruct-2407",
    "xai:grok-beta",
])
def test_timing_middleware_on_client(model_id):
    ctx = {}
    client = aibricks.client(model_id)
    client.add_middleware(TimingMiddleware(ctx))
    resp = client.chat.completions.create(model=None, messages=[{"role": "user", "content": "Tell me a joke."}])
    print(model_id, ctx)
    try:
        content = resp['choices'][0]['message']['content']
    except KeyError as e:
        print(resp)
        raise e
    assert content


@pytest.mark.parametrize("model_id", [
    "openai:gpt-4o-mini",
    "openrouter:meta-llama/llama-3.2-1b-instruct:free",
    "google:gemini-1.5-flash-8b",
    "arliai:Mistral-Nemo-12B-Instruct-2407",
    "xai:grok-beta",
])
def test_timing_middleware_on_connection(model_id):
    ctx = {}
    conn = aibricks.connect(model_id)
    conn.add_middleware(TimingMiddleware(ctx))
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(model_id, ctx)
    try:
        content = resp['choices'][0]['message']['content']
    except KeyError as e:
        print(resp)
        raise e
    assert content
