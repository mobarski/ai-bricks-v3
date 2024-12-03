from .openai_api import OpenAiConnection


class TogetherAiConnection(OpenAiConnection):
    api_key_env = "TOGETHER_API_KEY"
    api_base_url = "https://api.together.xyz/v1"
    provider = "togetherai"


if __name__ == "__main__":
    conn = TogetherAiConnection("meta-llama/Meta-Llama-3-8B-Instruct-Turbo")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
