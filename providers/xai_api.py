from openai_api import OpenAiHttpApi


class XaiHttpApi(OpenAiHttpApi):
    api_key_env = "XAI_API_KEY"
    api_base_url = "https://api.x.ai/v1"
    provider = "xai"


if __name__ == "__main__":
    model = XaiHttpApi("grok-beta")
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
