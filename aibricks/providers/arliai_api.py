from .openai_api import OpenAiConnection


# REF: https://www.arliai.com/docs
class ArliAiConnection(OpenAiConnection):
    api_key_env = "ARLIAI_API_KEY"
    api_base_url = "https://api.arliai.com/v1"
    provider = "arliai"


if __name__ == "__main__":
    conn = ArliAiConnection("Mistral-Nemo-12B-Instruct-2407")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
