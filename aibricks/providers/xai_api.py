from .openai_api import OpenAiConnection


class XaiConnection(OpenAiConnection):
    api_key_env = "XAI_API_KEY"
    api_base_url = "https://api.x.ai/v1"
    provider = "xai"


if __name__ == "__main__":
    conn = XaiConnection("grok-beta")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
