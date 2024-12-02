import os
import string

import yaml
import jinja2

# TODO: from environmental variables ???
# TODO: better names
# TODO: conver to list as the key is irrelevant ???
CONFIG_PATH = {
    'package': os.path.join(os.path.dirname(__file__), 'aibricks.yaml'),
    'system': '/etc/aibricks.yaml',
    'user': '~/.config/aibricks.yaml',
    'project': './aibricks.yaml'
}
MAX_ITERATIONS = 10


def load_config(path) -> dict[str, any]:
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.Loader)
    cfg = handle_include(cfg, path)
    return cfg


def load_all_configs() -> dict[str, dict]:
    return {k: load_config(v) for k, v in CONFIG_PATH.items()}


# TODO: design login for this
def merge_configs(configs: dict[str, dict]):
    return {k: v for k, v in configs.items() if v}


def handle_include(cfg, path):
    if 'include' not in cfg:
        return cfg

    for include in cfg['include']:
        include_path = os.path.join(os.path.dirname(path), include)
        chunk = load_config(include_path)
        # merge top level
        for k in cfg:
            # local values override included values
            if k not in chunk:
                chunk[k] = cfg[k]
            chunk[k].update(cfg[k])
        cfg = chunk

    del cfg['include']
    return cfg

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
_cfg = merge_configs(load_all_configs())


def lookup(key, default=..., _dict=_cfg):
    head, _, tail = key.partition('.')
    if head in _dict:
        return lookup(tail, default, _dict=_dict[head])
    elif default != ...:
        return default
    else:
        raise KeyError(key)


jinja2_env = jinja2.Environment(loader=jinja2.DictLoader(_cfg.get('templates', {})))


def render(text, **kwargs):
    return jinja2_env.from_string(text).render(**kwargs)


# TODO: rename variables -> export ???
# TODO: remove ???
def handle_variables(cfg, obj: any):
    if 'variables' not in cfg:
        return obj
    variables = cfg['variables']
    if isinstance(obj, str):
        text = obj
        for _ in range(MAX_ITERATIONS):
            text = string.Template(text).safe_substitute(variables)
        return text
    if isinstance(obj, list):
        return [handle_variables(cfg, x) for x in obj]
    if isinstance(obj, dict):
        return {k: handle_variables(cfg, v) for k, v in obj.items()}
    return obj


if __name__ == "__main__":
    from pprint import pprint
    configs = load_all_configs()
    for k, v in configs.items():
        pprint(handle_variables(v, v))
