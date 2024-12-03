import os
from functools import singledispatch

import yaml
import jinja2


# TODO: from environmental variables ???
def get_default_config_paths() -> list[str]:
    return [
        os.path.join(os.path.dirname(__file__), 'aibricks.yaml'),  # package
        '/etc/aibricks.yaml',                                      # system
        '~/.config/aibricks.yaml',                                 # user
        './aibricks.yaml'                                          # project
    ]


class Config:
    def __init__(self, data: dict):
        loader = jinja2.DictLoader(data.get('templates', {}))
        self.jinja2_env = jinja2.Environment(loader=loader)
        self.data = data

    def __repr__(self):
        return f'Config({self.data})'

    def lookup(self, key, default=..., _dict=None):
        _dict = _dict or self.data
        if not key:  # base case - we've consumed all parts
            return _dict
        
        head, _, tail = key.partition('.')
        if head in _dict:
            if isinstance(_dict[head], dict):
                return self.lookup(tail, default, _dict=_dict[head])
            elif not tail:  # it's a leaf node
                return _dict[head]
            elif default is not ...:
                return default
            else:
                raise KeyError(key)
        elif default is not ...:
            return default
        else:
            raise KeyError(key)

    def render(self, text, **kwargs):
        template = self.jinja2_env.from_string(text)
        return template.render(**kwargs)


def load_config(path) -> Config:
    if not os.path.exists(path):
        return Config({})
    with open(path, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.Loader) or {}
    cfg = handle_include(cfg, path)
    return Config(cfg)


def load_configs(config_paths: list[str] = None) -> list[Config]:
    paths = config_paths if config_paths is not None else get_default_config_paths()
    return [load_config(path) for path in paths]


# TODO: design logic for this
def merge_configs(configs: list[Config]) -> Config:
    """Merge configs with later configs taking precedence"""
    result = {}
    for config in reversed(configs):  # Explicit precedence order
        if config.data:
            result.update(config.data)
    return Config(result)


def handle_include(cfg, path):
    if not isinstance(cfg, dict) or 'include' not in cfg:
        return cfg

    for include in cfg['include']:
        include_path = os.path.join(os.path.dirname(path), include)
        chunk = load_config(include_path).data
        if not isinstance(chunk, dict):
            continue
        # merge top level
        for k in cfg:
            # local values override included values
            if k != 'include':  # skip the include key itself
                if k not in chunk:
                    chunk[k] = cfg[k]
                elif isinstance(cfg[k], dict) and isinstance(chunk[k], dict):
                    # only update if both values are dictionaries
                    chunk[k].update(cfg[k])
                else:
                    # for non-dict values, local values override included values
                    chunk[k] = cfg[k]
        cfg = chunk

    if 'include' in cfg:
        del cfg['include']
    return cfg


if __name__ == "__main__":
    cfgs = load_configs()
    print(cfgs)
    cfg = merge_configs(cfgs)
    print(cfg)
