from .openai_api import OpenAiConnection


class OpenRouterConnection(OpenAiConnection):
    api_key_env = "OPENROUTER_API_KEY"
    api_base_url = "https://openrouter.ai/api/v1"
    provider = "openrouter"


if __name__ == "__main__":
    conn = OpenRouterConnection("openai/gpt-3.5-turbo")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
