from .openai_api import OpenAiHttpApi


# REF: https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README.md
class LlamaCppHttpApi(OpenAiHttpApi):
    api_key_env = None
    api_base_url = "http://127.0.0.1:8080/v1"
    provider = "llamacpp"


if __name__ == "__main__":
    # TODO: test this
    model = LlamaCppHttpApi("llama-3.2-1b-instruct@q4_k_m")
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
