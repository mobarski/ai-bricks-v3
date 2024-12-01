from .openai_api import OpenAiConnection


class LmStudioConnection(OpenAiConnection):
    api_key_env = None
    api_base_url = "http://localhost:1234/v1"
    provider = "lmstudio"


if __name__ == "__main__":
    conn = LmStudioConnection("llama-3.2-1b-instruct@q4_k_m")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
