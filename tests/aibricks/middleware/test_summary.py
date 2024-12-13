from types import SimpleNamespace

import pytest

import aibricks
from aibricks.middleware import ChatSummaryMiddleware


MESSAGES = [
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
]


@pytest.mark.parametrize("model_id", [
    "dummy:aux",
    #"openai:gpt-4o-mini",
    #"openrouter:meta-llama/llama-3.2-1b-instruct:free",
    #"google:gemini-1.5-flash-8b",
    #"arliai:Mistral-Nemo-12B-Instruct-2407",
    #"xai:grok-beta",
])
def test_online_summary_max_chars(model_id):
    aux_connection = aibricks.connect(model_id)
    client = aibricks.connect('dummy:main')
    summary_middleware = ChatSummaryMiddleware(aux_connection, max_in_context_chars=20)
    summary_middleware.debug = True
    client.add_middleware(summary_middleware)
    resp = client.chat_create(MESSAGES)
    print(resp)
    print(client.ctx)


@pytest.mark.parametrize("model_id", [
    "dummy:aux",
    #"openai:gpt-4o-mini",
    #"openrouter:meta-llama/llama-3.2-1b-instruct:free",
    #"google:gemini-1.5-flash-8b",
    #"arliai:Mistral-Nemo-12B-Instruct-2407",
    #"xai:grok-beta",
])
def test_online_summary_command(model_id):
    aux_connection = aibricks.connect(model_id)
    client = aibricks.connect('dummy:main')
    summary_middleware = ChatSummaryMiddleware(aux_connection)
    summary_middleware.debug = True
    client.add_middleware(summary_middleware)
    resp = client.chat_create(MESSAGES + [{"role": "user", "content": "/summary"}])
    print(resp)
    print(client.ctx)
