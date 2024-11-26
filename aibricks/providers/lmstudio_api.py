from .openai_api import OpenAiHttpApi


class LmStudioHttpApi(OpenAiHttpApi):
    api_key_env = None
    api_base_url = "http://127.0.0.1:1234/v1"
    provider = "lmstudio"


if __name__ == "__main__":
    model = LmStudioHttpApi("llama-3.2-1b-instruct@q4_k_m")
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
