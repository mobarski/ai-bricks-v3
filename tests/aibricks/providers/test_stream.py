import pytest

import aibricks


@pytest.mark.parametrize("model_id", [
    "openai:gpt-4o-mini",
    "openrouter:meta-llama/llama-3.2-1b-instruct:free", # ERROR: Exception: Failed to parse response: : OPENROUTER PROCESSING
    "google:gemini-1.5-flash-8b",
    #"arliai:Mistral-Nemo-12B-Instruct-2407",
    "xai:grok-beta",
    "together:meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
])
def test_stream(model_id):
    print()
    conn = aibricks.connect(model_id)
    chunk_iter = conn.chat_create_stream([{"role": "user", "content": "Tell me a joke."}], stream=True)
    for chunk in chunk_iter:
        print(chunk)


def test_stream_demo():
    client = aibricks.client()
    resp = client.chat.completions.create(
        model='xai:grok-beta',
        messages=[{"role": "user", "content": "Tell me a joke."}],
        stream=True
    )
    for chunk in resp:
        #print(chunk)
        print(chunk['choices'][0]['delta'].get('content', ''), end="", flush=True)
