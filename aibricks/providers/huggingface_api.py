from .openai_api import OpenAiConnection


# REF: https://huggingface.co/docs/api-inference/getting-started
# REF: https://huggingface.co/blog/tgi-messages-api
# TODO

class HuggingFaceConnection(OpenAiConnection):
    api_key_env = "HUGGINGFACE_API_KEY"
    api_base_url = "https://api-inference.huggingface.co/models"
    provider = "huggingface"


if __name__ == "__main__":
    conn = HuggingFaceConnection("TODO")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
