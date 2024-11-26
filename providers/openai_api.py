import json
import os

import requests

# REF: https://github.com/andrewyng/aisuite/blob/main/aisuite/providers/openai_provider.py
# REF:https://platform.openai.com/docs/api-reference/chat/create


class OpenAiHttpApi:
    api_key_env = "OPENAI_API_KEY"
    api_base_url = "https://api.openai.com/v1"
    provider = "openai"

    def __init__(self, model, **kwargs):
        self.model = model
        self.kwargs = kwargs

    def chat_create(self, messages, **kwargs):
        data = {
            'model': self.model,
            'messages': messages,
            **{**self.kwargs, **kwargs}
        }
        raw_resp = requests.post(
            url=f"{self.api_base_url}/chat/completions",
            headers=self.headers(),
            data=json.dumps(data)
        )
        return self.normalized_response(raw_resp)

    def headers(self):
        return {
            "Authorization": f"Bearer {self.api_key()}",
            "Content-Type": "application/json",
        }

    def api_key(self):
        return os.getenv(self.api_key_env) if self.api_key_env else 'NO-API-KEY-SET'

    def normalized_response(self, raw_resp):
        resp = self.parse_response(raw_resp)
        return resp

    def parse_response(self, raw_resp):
        try:
            resp = raw_resp.json()
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse response: {raw_resp.text}")
        return resp


if __name__ == "__main__":
    model = OpenAiHttpApi("gpt-3.5-turbo")
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
