from openai_api import OpenAiHttpApi


class OpenRouterHttpApi(OpenAiHttpApi):
    api_key_env = "OPENROUTER_API_KEY"
    api_base_url = "https://openrouter.ai/api/v1"
    provider = "openrouter"


if __name__ == "__main__":
    model = OpenRouterHttpApi("openai/gpt-3.5-turbo")
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
