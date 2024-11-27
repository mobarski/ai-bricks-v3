## About

Simple, unified interface to multiple Generative AI providers.

This project is similar in scope to [AISuite](https://github.com/andrewyng/aisuite),
but with the following differences:
- streamlined API (still similar to OpenAI's)
- configuration driven (yaml)
- minimal dependencies:`requests`, `pyyaml`

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
| KoboldCPP  | `koboldcpp:` | - |
| LlamaCPP   | `llamacpp:` | - |

## Installation

Don't. It's still in the experimental phase.

## How to use


```python
import aibricks

model = aibricks.connect('openrouter:qwen/qwen-2.5-coder-32b-instruct')
resp = model.chat_create([{"role": "user", "content": "Tell me a joke."}])
print(resp)
```

How to test the provider API:
```sh
python3 -m aibricks.providers.lmstudio_api
```

## License

MIT

