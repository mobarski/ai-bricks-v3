from .openai_api import OpenAiHttpApi


# REF: https://ollama.com/blog/openai-compatibility
class OllamaHttpApi(OpenAiHttpApi):
    api_key_env = None
    api_base_url = "http://127.0.0.1:11434/v1"
    provider = "ollama"


if __name__ == "__main__":
    # TODO: test this
    model = OllamaHttpApi("llama-3.2-1b-instruct@q4_k_m")
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
