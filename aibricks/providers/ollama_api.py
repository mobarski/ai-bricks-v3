from .openai_api import OpenAiConnection


# REF: https://ollama.com/blog/openai-compatibility
class OllamaConnection(OpenAiConnection):
    api_key_env = None
    api_base_url = "http://localhost:11434/v1"
    provider = "ollama"


if __name__ == "__main__":
    conn = OllamaConnection("qwen2.5-coder:7b")
    resp = conn.chat_create([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
