from .openai_api import OpenAiConnection


# REF: https://ai.google.dev/gemini-api/docs/openai
class GoogleConnection(OpenAiConnection):
    api_key_env = "GOOGLE_API_KEY"
    api_base_url = "https://generativelanguage.googleapis.com/v1beta"
    provider = "google"


if __name__ == "__main__":
    conn = GoogleConnection("gemini-1.5-flash")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
