from .providers import PROVIDER_MAPPING
from .middleware import MIDDLEWARE_MAPPING


def connect(connection_str=None, **kwargs):
    assert connection_str or (kwargs.get('from_config') and kwargs.get('config'))

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

    if provider not in PROVIDER_MAPPING:
        raise ValueError(f"Unknown provider: {provider}")

    return PROVIDER_MAPPING[provider](model, **kwargs)


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
            if middleware_name not in MIDDLEWARE_MAPPING:
                raise ValueError(f"Unknown middleware: {middleware_name}")

            # Handle nested connection configuration
            if middleware_params and 'connection' in middleware_params:
                conn_config = middleware_params['connection']
                if isinstance(conn_config, dict) and 'from_config' in conn_config:
                    middleware_params['connection'] = connect(
                        from_config=conn_config['from_config'],
                        config=config
                    )

            # Create and add middleware instance
            middleware_class = MIDDLEWARE_MAPPING[middleware_name]
            middleware_instance = middleware_class(**middleware_params)
            conn.add_middleware(middleware_instance)

    return conn
