import os
from aibricks.config import load_config

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_data/config')


def test_load_base_config():
    cfg = load_config(os.path.join(TEST_DATA_DIR, 'base.yaml'))
    assert cfg.lookup('model.name') == 'gpt-4'
    assert cfg.lookup('model.temperature') == 0.7
    assert cfg.lookup('model.max_tokens') == 2000
    assert cfg.lookup('api.base_url') == 'https://api.example.com'


def test_include_config():
    cfg = load_config(os.path.join(TEST_DATA_DIR, 'include.yaml'))
    # Check if values from include.yaml override base.yaml
    assert cfg.lookup('model.name') == 'gpt-3.5-turbo'
    assert cfg.lookup('model.max_tokens') == 4000
    # Check if non-overridden values from base.yaml are preserved
    assert cfg.lookup('model.temperature') == 0.7
    assert cfg.lookup('api.base_url') == 'https://api.example.com'


def test_template_rendering():
    cfg = load_config(os.path.join(TEST_DATA_DIR, 'base.yaml'))
    rendered = cfg.render('system_prompt', name='TestBot', role='coding assistant')
    assert 'You are an AI assistant named TestBot' in rendered
    assert 'Your role is: coding assistant' in rendered
