from .client import Client
from .providers import (
    DummyConnection, OpenAiConnection, OpenRouterConnection,
    TabbyApiConnection, ArliAiConnection, XaiConnection,
    LlamaCppConnection, KoboldCppConnection, LmStudioConnection,
    HuggingFaceConnection, GoogleConnection, OllamaConnection
)


def connect(connection_str, **kwargs):
    provider, model = connection_str.split(":", 1)
    if provider == "dummy":
        return DummyConnection(model, **kwargs)
    if provider == "openai":
        return OpenAiConnection(model, **kwargs)
    if provider == "openrouter":
        return OpenRouterConnection(model, **kwargs)
    if provider == "tabbyapi":
        return TabbyApiConnection(model, **kwargs)
    if provider == "arliai":
        return ArliAiConnection(model, **kwargs)
    if provider == "xai":
        return XaiConnection(model, **kwargs)
    if provider == "llamacpp":
        return LlamaCppConnection(model, **kwargs)
    if provider == "koboldcpp":
        return KoboldCppConnection(model, **kwargs)
    if provider == "lmstudio":
        return LmStudioConnection(model, **kwargs)
    if provider == "huggingface":
        return HuggingFaceConnection(model, **kwargs)
    if provider == "google":
        return GoogleConnection(model, **kwargs)
    if provider == "ollama":
        return OllamaConnection(model, **kwargs)
    raise ValueError(f"Unknown provider: {provider}")


def client(model=None, **kwargs):
    return Client(connect, model, **kwargs)
