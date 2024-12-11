import json
import time

from .openai_api import OpenAiConnection


class DummyConnection(OpenAiConnection):
    api_key_env = None
    api_base_url = None
    provider = "dummy"

    def post_request(self, **kwargs):
        data = json.loads(kwargs["data"])
        model = data["model"]
        messages = data["messages"]
        return DummyResponse(model, messages)


class DummyResponse:
    def __init__(self, model, messages):
        self.model = model
        self.messages = messages

    def json(self):
        return {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": self.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"DUMMY RESPONSE to {len(self.messages)} messages ({len(str(self.messages))} characters) from the {self.model} model"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 9,
                "completion_tokens": 12,
                "total_tokens": 21
            }
        }


if __name__ == "__main__":
    conn = DummyConnection("WHATEVER")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
