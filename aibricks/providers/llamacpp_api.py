from .openai_api import OpenAiConnection


# REF: https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README.md
class LlamaCppConnection(OpenAiConnection):
    api_key_env = None
    api_base_url = "http://localhost:8080/v1"
    provider = "llamacpp"


if __name__ == "__main__":
    # TODO: test this
    conn = LlamaCppConnection("llama-3.2-1b-instruct@q4_k_m")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
