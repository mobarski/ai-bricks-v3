import pytest

import aibricks


@pytest.mark.parametrize("model_id", [
    "openai:gpt-4o-mini",
    "openrouter:meta-llama/llama-3.2-1b-instruct:free",
    "google:gemini-1.5-flash-8b",
    "arliai:Mistral-Nemo-12B-Instruct-2407",
    "xai:grok-beta",
])
def test_online_provider(model_id):
    model = aibricks.connect(model_id)
    model.middleware.append(aibricks.middleware.TimingMiddleware())
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    try:
        content = resp['choices'][0]['message']['content']
    except KeyError as e:
        print(resp)
        raise e
    assert content
