from .openai_api import OpenAiConnection


class TogetherConnection(OpenAiConnection):
    api_key_env = "TOGETHER_API_KEY"
    api_base_url = "https://api.together.xyz/v1"
    provider = "together"


if __name__ == "__main__":
    conn = TogetherConnection("meta-llama/Meta-Llama-3-8B-Instruct-Turbo")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
