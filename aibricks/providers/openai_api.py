import json
import os

import requests

from ..middleware import MiddlewareMixin, MiddlewareContext

# REF: https://github.com/andrewyng/aisuite/blob/main/aisuite/providers/openai_provider.py
# REF:https://platform.openai.com/docs/api-reference/chat/create


class OpenAiHttpApi(MiddlewareMixin):
    api_key_env = "OPENAI_API_KEY"
    api_base_url = "https://api.openai.com/v1"
    provider = "openai"

    def __init__(self, model, **kwargs):
        self.model = model
        self.kwargs = kwargs

    def chat_create(self, messages, **kwargs):
        ctx = MiddlewareContext()
        data = self.normalized_data(messages, **kwargs)
        data = self.run_middleware("data", ctx, data)
        # ------------------------------------------------
        raw_resp = requests.post(
            url=f"{self.api_base_url}/chat/completions",
            headers=self.headers(),
            data=json.dumps(data)
        )
        # ------------------------------------------------
        raw_resp = self.run_middleware("raw_resp", ctx, raw_resp)
        resp = self.parse_response(raw_resp)
        resp = self.run_middleware("resp", ctx, resp)
        norm_resp = self.normalize_response(resp)
        norm_resp = self.run_middleware("norm_resp", ctx, norm_resp)
        return norm_resp

    def headers(self):
        return {
            "Authorization": f"Bearer {self.api_key()}",
            "Content-Type": "application/json",
        }

    def api_key(self):
        if self.api_key_env:
            api_key = os.getenv(self.api_key_env)
            if not api_key:
                raise Exception(f"environment variable {self.api_key_env} is not set")
            return api_key
        return "NO-API-KEY-SET"

    def normalized_data(self, messages, **kwargs):
        return {
            'model': self.model,
            'messages': messages,
            **{**self.kwargs, **kwargs}
        }

    def normalize_response(self, resp):
        return resp

    def parse_response(self, raw_resp):
        try:
            resp = raw_resp.json()
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse response: {raw_resp.text}")
        return resp

"""
def my_wrapper(ctx):
    t0 = time.time()
    ctx.fun(*ctx.args, **ctx.kwargs)
    ctx.duration = time.time() - t0
"""

if __name__ == "__main__":
    model = OpenAiHttpApi("gpt-3.5-turbo")
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
