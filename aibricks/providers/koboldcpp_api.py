from .openai_api import OpenAiHttpApi


# REF: https://lite.koboldai.net/koboldcpp_api
class KoboldCppHttpApi(OpenAiHttpApi):
    api_key_env = None
    api_base_url = "http://127.0.0.1:5001/v1"
    provider = "koboldcpp"


if __name__ == "__main__":
    model = KoboldCppHttpApi(None)
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
