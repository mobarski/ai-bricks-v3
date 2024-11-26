import json
import os

import requests

from .openai_api import OpenAiHttpApi


class TabbyApiHttpApi(OpenAiHttpApi):
    api_key_env = 'TABBY_API_KEY'
    admin_key_env = 'TABBY_ADMIN_KEY'
    hf_api_token_env = 'HF_API_TOKEN'
    api_base_url = "http://127.0.0.1:5000/v1"
    provider = "tabbyapi"

    def download_model(self, repo_id, folder_name='', revision='main', **kwargs):
        data = {
            "repo_id": repo_id,
            "folder_name": folder_name,
            "revision": revision,
            "token": os.getenv(self.hf_api_token_env),
            **kwargs
        }
        raw_resp = requests.post(
            url=f"{self.api_base_url}/download",
            headers={
                "x-admin-key": os.getenv(self.admin_key_env),
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
        )
        return raw_resp.json()

    def load_model(self, model_name, **kwargs):
        data = {
            "model_name": model_name,
            **kwargs
        }
        raw_resp = requests.post(
            url=f"{self.api_base_url}/model/load",
            headers={
                "x-admin-key": os.getenv(self.admin_key_env),
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
        )
        return raw_resp # TODO: cannot pare response - problem on the server side


if __name__ == "__main__":
    model = TabbyApiHttpApi(None)
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
    resp = model.download_model("lucyknada/Qwen_Qwen2.5-Coder-0.5B-Instruct-exl2", revision="4.0bpw")
    print(resp)
    resp = model.load_model("Qwen_Qwen2.5-Coder-0.5B-Instruct-exl2")
    print(resp)
