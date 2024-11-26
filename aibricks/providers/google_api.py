from .openai_api import OpenAiHttpApi


# REF: https://ai.google.dev/gemini-api/docs/openai
class GoogleHttpApi(OpenAiHttpApi):
    api_key_env = "GEMINI_API_KEY"
    api_base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
    provider = "google"


if __name__ == "__main__":
    model = GoogleHttpApi("gemini-1.5-flash")
    resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
