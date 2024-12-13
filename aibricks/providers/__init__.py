from .openai_api import OpenAiConnection
from .dummy_api import DummyConnection
from .openai_api import OpenAiConnection
from .openrouter_api import OpenRouterConnection
from .tabbyapi_api import TabbyApiConnection
from .arliai_api import ArliAiConnection
from .xai_api import XaiConnection
from .llamacpp_api import LlamaCppConnection
from .koboldcpp_api import KoboldCppConnection
from .lmstudio_api import LmStudioConnection
from .huggingface_api import HuggingFaceConnection
from .google_api import GoogleConnection
from .ollama_api import OllamaConnection
from .together_api import TogetherConnection

# create mapping from provider name to provider class
PROVIDER_MAPPING = {
    "dummy": DummyConnection,
    "openai": OpenAiConnection,
    "openrouter": OpenRouterConnection,
    "tabbyapi": TabbyApiConnection,
    "arliai": ArliAiConnection,
    "xai": XaiConnection,
    "llamacpp": LlamaCppConnection,
    "koboldcpp": KoboldCppConnection,
    "lmstudio": LmStudioConnection,
    "huggingface": HuggingFaceConnection,
    "google": GoogleConnection,
    "ollama": OllamaConnection,
    "together": TogetherConnection,
}
