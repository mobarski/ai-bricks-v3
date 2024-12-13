from .client import Client
from .providers import (
    DummyConnection, OpenAiConnection, OpenRouterConnection,
    TabbyApiConnection, ArliAiConnection, XaiConnection,
    LlamaCppConnection, KoboldCppConnection, LmStudioConnection,
    HuggingFaceConnection, GoogleConnection, OllamaConnection,
    TogetherConnection,
)

from .middleware import (
    TimingMiddleware, LoggingMiddleware,
    ChatSummaryMiddleware, SaveLoadMiddleware
)

from .config import load_config, Config

# Map middleware class names to actual classes
MIDDLEWARE_CLASSES = {
    'TimingMiddleware': TimingMiddleware,
    'LoggingMiddleware': LoggingMiddleware,
    'ChatSummaryMiddleware': ChatSummaryMiddleware,  # noqa
    'SaveLoadMiddleware': SaveLoadMiddleware,
}


def connect(connection_str=None, **kwargs):
    assert connection_str or (kwargs.get('from_config') and kwargs.get('config'))  # noqa

    config = kwargs.pop('config', None)
    active = kwargs.pop('from_config', None)
    if config and active:
        return _create_connection_from_config(config, active, **kwargs)

    return _create_connection(connection_str, **kwargs)


def _create_connection(connection_str, **kwargs):
    # Handle normal case
    if ':' in connection_str:
        provider, model = connection_str.split(":", 1)
    else:
        provider = connection_str
        model = ''  # TODO: or None ???

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
    if provider == "together":
        return TogetherConnection(model, **kwargs)
    raise ValueError(f"Unknown provider: {provider}")


def _create_connection_from_config(config, active, **kwargs):
    connection_str = config.lookup(f'{active}.connection_str')
    cfg_kwargs = config.lookup(f'{active}.kwargs', {})
    kwargs = {**cfg_kwargs, **kwargs}

    # Create connection first
    conn = _create_connection(connection_str, **kwargs)

    # Handle middleware if specified in config
    middleware_configs = config.lookup(f'{active}.middleware', [])
    for middleware_config in middleware_configs:
        for middleware_name, middleware_params in middleware_config.items():
            middleware_params = middleware_params or {}
            if middleware_name not in MIDDLEWARE_CLASSES:
                raise ValueError(f"Unknown middleware: {middleware_name}")

            # Handle nested connection configuration
            if middleware_params and 'connection' in middleware_params:
                conn_config = middleware_params['connection']
                if 'from_config' in conn_config:
                    middleware_params['connection'] = connect(
                        from_config=conn_config['from_config'],
                        config=config
                    )

            # Create and add middleware instance
            middleware_class = MIDDLEWARE_CLASSES[middleware_name]
            middleware_instance = middleware_class(**middleware_params)
            conn.add_middleware(middleware_instance)

    return conn


def client(model=None, **kwargs):
    return Client(connect, model, **kwargs)
