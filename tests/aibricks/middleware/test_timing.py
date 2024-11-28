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
def test_online_provider(model_id):
    ctx = SimpleNamespace()
    model = aibricks.connect(model_id)
    model.middleware.append(TimingMiddleware(ctx))
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print('middleware-duration:', model_id, ctx.duration)
    try:
        content = resp['choices'][0]['message']['content']
    except KeyError as e:
        print(resp)
        raise e
    assert content
