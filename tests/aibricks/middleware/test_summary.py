from types import SimpleNamespace

import pytest

import aibricks
from aibricks.middleware import ChatSummaryMiddleware


@pytest.mark.parametrize("model_id", [
    #"openai:gpt-4o-mini",
    #"openrouter:meta-llama/llama-3.2-1b-instruct:free",
    #"google:gemini-1.5-flash-8b",
    #"arliai:Mistral-Nemo-12B-Instruct-2407",
    "xai:grok-beta",
])
def test_online_provider(model_id):
    ctx = {}
    aux_client = aibricks.connect(model_id)
    client = aibricks.connect('dummy:')
    summary_middleware = ChatSummaryMiddleware(ctx, aux_client, max_in_context_chars=20)
    client.add_middleware(summary_middleware)
    resp = client.chat_create([
        {"role": "user", "content": "Tell me a joke."},
        {"role": "assistant", "content": '''Why did the scarecrow win an award?\n\nBecause he was outstanding in his field!'''},
        {"role": "user", "content": "Tell me a joke."},
        {"role": "assistant", "content": '''A man walked into a library and asked the librarian, "Do you have any books on Pavlov's dogs and Schrödinger's cat?" The librarian replied, "It rings a bell, but I'm not sure if it's here or not."'''},
        {"role": "user", "content": "Tell me a joke."},
        {"role": "assistant", "content": '''Why don't scientists trust atoms?\n\nBecause they make up everything!'''},    
        {"role": "user", "content": "Tell me a joke."},
        {"role": "assistant", "content": '''What do you call a fake noodle?\n\nAn impasta!'''},
        {"role": "user", "content": "Tell me a joke."},
        {"role": "assistant", "content": '''Why don't scientists trust atoms?\n\nBecause they make up everything!'''},
    ])
    print(resp)
    print(ctx)
