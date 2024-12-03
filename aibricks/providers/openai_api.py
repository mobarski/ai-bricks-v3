import json
import os

import requests

from ..middleware import MiddlewareMixin

# REF: https://github.com/andrewyng/aisuite/blob/main/aisuite/providers/openai_provider.py
# REF:https://platform.openai.com/docs/api-reference/chat/create


class OpenAiConnection(MiddlewareMixin):
    api_key_env = "OPENAI_API_KEY"
    api_base_url = "https://api.openai.com/v1"
    provider = "openai"

    def __init__(self, model, **kwargs):
        self.model = model
        self.kwargs = kwargs

    # TODO: rename ???
    def chat_create(self, messages, **kwargs):
        data = self.normalized_chat_data(messages, **kwargs)
        request = self.normalized_chat_request(data)
        request = self.run_middleware("request", request)
        request['data'] = json.dumps(data)  # done here to allow data modification
        # -------------------------------
        raw_resp = self.post_request(**request)
        # -------------------------------
        raw_resp = self.run_middleware("raw_response", raw_resp)
        resp = self.parse_response(raw_resp)
        resp = self.run_middleware("response", resp)
        norm_resp = self.normalize_response(resp)
        norm_resp = self.run_middleware("normalized_response", norm_resp)
        return norm_resp

    # WIP
    def chat_create_stream(self, messages, **kwargs):
        data = self.normalized_chat_data(messages, **kwargs)
        request = self.normalized_chat_request(data)
        request = self.run_middleware("request", request)
        request['data'] = json.dumps(data)  # done here to allow data modification
        # --------------------------------------
        raw_resp = self.post_request(**request)
        # --------------------------------------
        for line in raw_resp.iter_lines():
            line = line.decode("utf-8").strip()
            if line == "data: [DONE]":
                break
            if line.startswith("data: {"):
                raw_data = line[5:]
                resp = json.loads(raw_data)
                #resp = self.parse_response(raw_data)
                #resp = self.run_middleware("response", resp)
                #norm_resp = self.normalize_response(resp)
                #norm_resp = self.run_middleware("normalized_response", norm_resp)
                yield resp


    def post_request(self, **kwargs):
        return requests.post(**kwargs)

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

    # TODO: combine with normalized_chat_request ???
    def normalized_chat_data(self, messages, **kwargs):
        return {
            'model': self.model,
            'messages': messages,
            **{**self.kwargs, **kwargs}
        }

    # TODO: combine with normalized_chat_data ???
    def normalized_chat_request(self, data):
        return dict(
            url=f"{self.api_base_url}/chat/completions",
            headers=self.headers(),
            data=data,
        )

    def normalize_response(self, resp):
        return resp

    def parse_response(self, raw_resp):
        try:
            resp = raw_resp.json()
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse response: {raw_resp.text}")
        return resp


if __name__ == "__main__":
    conn = OpenAiConnection("gpt-3.5-turbo")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
