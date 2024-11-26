def connect(model_str, **kwargs):
    provider, model = model_str.split(":", 1)
    if provider == "openai":
        from .providers.openai_api import OpenAiHttpApi
        return OpenAiHttpApi(model, **kwargs)
    if provider == "openrouter":
        from .providers.openrouter_api import OpenRouterHttpApi
        return OpenRouterHttpApi(model, **kwargs)
    if provider == "tabbyapi":
        from .providers.tabbyapi_api import TabbyApiHttpApi
        return TabbyApiHttpApi(model, **kwargs)
    if provider == "arliai":
        from .providers.arliai_api import ArliAiHttpApi
        return ArliAiHttpApi(model, **kwargs)
    if provider == "xai":
        from .providers.xai_api import XaiHttpApi
        return XaiHttpApi(model, **kwargs)
    if provider == "llamacpp":
        from .providers.llamacpp_api import LlamaCppHttpApi
        return LlamaCppHttpApi(model, **kwargs)
    if provider == "koboldcpp":
        from .providers.koboldcpp_api import KoboldCppHttpApi
        return KoboldCppHttpApi(model, **kwargs)
    if provider == "lmstudio":
        from .providers.lmstudio_api import LmStudioHttpApi
        return LmStudioHttpApi(model, **kwargs)
    if provider == "google":
        from .providers.google_api import GoogleHttpApi
        return GoogleHttpApi(model, **kwargs)
    raise Exception(f"Unknown provider: {provider}")
