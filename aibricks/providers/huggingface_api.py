from .openai_api import OpenAiHttpApi

# REF: https://huggingface.co/docs/api-inference/getting-started
# REF: https://huggingface.co/blog/tgi-messages-api
# TODO
class HuggingFaceHttpApi(OpenAiHttpApi):
    api_key_env = "HF_API_TOKEN"
    api_base_url = "TODO"
    provider = "huggingface"


if __name__ == "__main__":
    model = HuggingFaceHttpApi("TODO")
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
