## About

Simple, unified interface to multiple Generative AI providers.


## Supported providers

| Provider   | Example Model String | Environmental Variables |
|------------|----------------------|------------------------------|
| OpenAI     | `openai:gpt-3.5-turbo` | OPENAI_API_KEY |
| Google     | `google:gemini-1.5-flash` | GEMINI_API_KEY |
| OpenRouter | `openrouter:openai/gpt-3.5-turbo` | OPENROUTER_API_KEY |
| ArliAI     | `arliai:Mistral-Nemo-12B-Instruct-2407` | ARLIAI_API_KEY |
| XAI        | `xai:grok-beta` | XAI_API_KEY |
| LMStudio   | `lmstudio:` | N/A |
| tabbyAPI   | `tabbyapi:` | TABBYAPI_API_KEY<br>TABBYAPI_ADMIN_KEY<br>HF_HUB_TOKEN |
| KoboldCPP  | `koboldcpp:` | N/A |
| LlamaCPP   | `llamacpp:` | N/A |

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

