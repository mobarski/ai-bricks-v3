from types import SimpleNamespace
import sqlite3

import pytest

import aibricks
from aibricks.middleware import LoggingMiddleware


@pytest.mark.parametrize("model_id", [
    "openai:gpt-4o-mini",
    "openrouter:meta-llama/llama-3.2-1b-instruct:free",
    "google:gemini-1.5-flash-8b",
    "arliai:Mistral-Nemo-12B-Instruct-2407",
    "xai:grok-beta",
])
def test_online_provider(model_id):
    ctx = {}
    db = sqlite3.connect(":memory:")
    client = aibricks.connect(model_id)
    client.add_middleware(LoggingMiddleware(ctx, db=db))
    _ = client.chat_create([{"role": "user", "content": "Tell me a joke."}])
    rows = db.execute("SELECT * FROM logs").fetchall()
    print(rows)
