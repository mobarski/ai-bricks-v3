from .openai_api import OpenAiConnection


# REF: https://lite.koboldai.net/koboldcpp_api
class KoboldCppConnection(OpenAiConnection):
    api_key_env = None
    api_base_url = "http://localhost:5001/v1"
    provider = "koboldcpp"


if __name__ == "__main__":
    conn = KoboldCppConnection(None)
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
