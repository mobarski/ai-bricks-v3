from openai_api import OpenAiHttpApi


# REF: https://www.arliai.com/docs
class ArliAiHttpApi(OpenAiHttpApi):
    api_key_env = "ARLIAI_API_KEY"
    api_base_url = "https://api.arliai.com/v1"
    provider = "arliai"


if __name__ == "__main__":
    model = ArliAiHttpApi("Mistral-Nemo-12B-Instruct-2407")
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
