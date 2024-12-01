import json

from .openai_api import OpenAiConnection


# REF: https://github.com/theroyallab/tabbyAPI/wiki/API-Reference
# REF: https://github.com/theroyallab/tabbyAPI/wiki/API-Reference#chat-completion
# REF: https://github.com/theroyallab/tabbyAPI/wiki/API-Reference#model-management
class TabbyApiConnection(OpenAiConnection):
    api_key_env = None
    api_base_url = "http://localhost:5001/v1"
    provider = "tabbyapi"

    def normalized_chat_data(self, messages, **kwargs):
        data = super().normalized_chat_data(messages, **kwargs)
        data["messages"] = [{"role": m["role"], "content": m["content"]} for m in messages]
        return data

    def download_model(self, model, revision=None):
        data = {"name": model}
        if revision:
            data["revision"] = revision
        request = {
            "url": f"{self.api_base_url}/model/download",
            "headers": self.headers(),
            "data": json.dumps(data),
        }
        raw_resp = self.post_request(**request)
        return raw_resp.json()

    def load_model(self, model):
        data = {"name": model}
        request = {
            "url": f"{self.api_base_url}/model/load",
            "headers": self.headers(),
            "data": json.dumps(data),
        }
        raw_resp = self.post_request(**request)
        return raw_resp.json()


if __name__ == "__main__":
    conn = TabbyApiConnection(None)
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
    resp = conn.download_model("lucyknada/Qwen_Qwen2.5-Coder-0.5B-Instruct-exl2", revision="4.0bpw")
    print(resp)
    resp = conn.load_model("Qwen_Qwen2.5-Coder-0.5B-Instruct-exl2")
    print(resp)
