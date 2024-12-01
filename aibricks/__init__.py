from .client import Client


def connect(connection_str, **kwargs):
    provider, model = connection_str.split(":", 1)
    if provider == "dummy":
        from .providers.dummy_api import DummyConnection
        return DummyConnection(model, **kwargs)
    if provider == "openai":
        from .providers.openai_api import OpenAiConnection
        return OpenAiConnection(model, **kwargs)
    if provider == "openrouter":
        from .providers.openrouter_api import OpenRouterConnection
        return OpenRouterConnection(model, **kwargs)
    if provider == "tabbyapi":
        from .providers.tabbyapi_api import TabbyApiConnection
        return TabbyApiConnection(model, **kwargs)
    if provider == "arliai":
        from .providers.arliai_api import ArliAiConnection
        return ArliAiConnection(model, **kwargs)
    if provider == "xai":
        from .providers.xai_api import XaiConnection
        return XaiConnection(model, **kwargs)
    if provider == "llamacpp":
        from .providers.llamacpp_api import LlamaCppConnection
        return LlamaCppConnection(model, **kwargs)
    if provider == "koboldcpp":
        from .providers.koboldcpp_api import KoboldCppConnection
        return KoboldCppConnection(model, **kwargs)
    if provider == "lmstudio":
        from .providers.lmstudio_api import LmStudioConnection
        return LmStudioConnection(model, **kwargs)
    if provider == "huggingface":
        from .providers.huggingface_api import HuggingFaceConnection
        return HuggingFaceConnection(model, **kwargs)
    if provider == "google":
        from .providers.google_api import GoogleConnection
        return GoogleConnection(model, **kwargs)
    if provider == "ollama":
        from .providers.ollama_api import OllamaConnection
        return OllamaConnection(model, **kwargs)
    raise ValueError(f"Unknown provider: {provider}")


def client(model=None, **kwargs):
    return Client(connect, model, **kwargs)
