import os
import pytest
from aibricks.config import load_config, handle_variables, render

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


def test_variables():
    cfg = load_config(os.path.join(TEST_DATA_DIR, 'variables.yaml'))
    # Test variable substitution
    cfg = handle_variables(cfg, cfg)
    assert cfg.lookup('model.name') == 'gpt-4'
    assert cfg.lookup('model.url') == 'https://api.openai.com/v1/chat/completions'

    # Test environment variable substitution
    os.environ['OPENAI_API_KEY'] = 'test-api-key'
    cfg = load_config(os.path.join(TEST_DATA_DIR, 'variables.yaml'))
    cfg = handle_variables(cfg, cfg)
    assert cfg.lookup('model.api_key') == 'test-api-key'


def test_template_rendering():
    cfg = load_config(os.path.join(TEST_DATA_DIR, 'base.yaml'))
    rendered = render(cfg.lookup('templates.system_prompt'), 
                     name='TestBot',
                     temperature=0.8)
    assert 'You are an AI assistant named TestBot' in rendered
    assert 'Temperature is set to 0.8' in rendered
