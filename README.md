## About

Simple, unified interface to multiple Generative AI providers.

This project is similar in scope to [AISuite](https://github.com/andrewyng/aisuite),
but with the following differences:
- minimal dependencies (requests, pyyaml)
- stronger support for local models (tabbyAPI, KoboldCpp, ...)
- wrapper infrastructure for logging, usage, pricing, styling, etc
- configuration driven (yaml + string.Template)

## Supported providers

| Provider   | Example Connection String | Environmental Variables |
|------------|----------------------|------------------------------|
| OpenAI     | `openai:gpt-3.5-turbo` | OPENAI_API_KEY |
| Google     | `google:gemini-1.5-flash` | GEMINI_API_KEY |
| OpenRouter | `openrouter:openai/gpt-3.5-turbo` | OPENROUTER_API_KEY |
| ArliAI     | `arliai:Mistral-Nemo-12B-Instruct-2407` | ARLIAI_API_KEY |
| XAI        | `xai:grok-beta` | XAI_API_KEY |
| tabbyAPI   | `tabbyapi:` | TABBYAPI_API_KEY<br>TABBYAPI_ADMIN_KEY<br>HF_API_TOKEN |
| Ollama     | `ollama:qwen2.5-coder:7b` | - |
| LMStudio   | `lmstudio:` | - |
| KoboldCpp  | `koboldcpp:` | - |
| LlamaCpp   | `llamacpp:` | - |

## Installation

Don't. It's still in the experimental phase.

## How to use


```python
import aibricks

# OpenAI drop in replacement
client = aibricks.client()
resp = client.chat.completions.create(
    model='openrouter:qwen/qwen-2.5-coder-32b-instruct',
    messages=[{"role": "user", "content": "Tell me a joke."}],
    temperature=0.7
)
print(resp)

# with default parameters
client = aibricks.client(
    model='openrouter:qwen/qwen-2.5-coder-32b-instruct',
    temperature=0.7
)
resp = client.chat.completions.create(
    model='IGNORED',
    messages=[{"role": "user", "content": "Tell me a joke."}],
)
print(resp)

```

## How to test

```sh
# Run simple connection test for a specific provider
python3 -m aibricks.providers.lmstudio_api

# Run all tests
pytest tests/

# Run only config tests
pytest tests/aibricks/config/

# Run only provider tests
pytest tests/aibricks/providers/
```

## License

MIT

