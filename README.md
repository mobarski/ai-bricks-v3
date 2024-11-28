## AI Bricks

Simple, unified interface to multiple Generative AI providers and local model servers.

This project is similar in scope to [AISuite](https://github.com/andrewyng/aisuite),
but with the following differences:
- stronger support for local model servers (*tabbyAPI*, *KoboldCpp*, *LMStudio*, *Ollama*, ...)
- focused on improving your application without having to change your code
- middleware for logging, usage tracking, styling, etc
- minimal dependencies (*requests*, *pyyaml*)


## Supported providers

| Provider     | Example Connection String     | Environmental Variables  | Notes |
|--------------|-------------------------------|--------------------------|-------|
| *OpenAI*     | `openai:gpt-4o-mini`          | OPENAI_API_KEY           |       |
| *Google*     | `google:gemini-1.5-flash`     | GEMINI_API_KEY           |       |
| *OpenRouter* | `openrouter:openai/gpt-4o`    | OPENROUTER_API_KEY       |       |
| *ArliAI*     | `arliai:Llama-3.1-70B-Tulu-2` | ARLIAI_API_KEY           |       |
| *XAI*        | `xai:grok-beta`               | XAI_API_KEY              |       |
| *Ollama*     | `ollama:qwen2.5-coder:7b`     | -                        | GGUF  |
| *LMStudio*   | `lmstudio:`                   | -                        | GGUF  |
| *KoboldCpp*  | `koboldcpp:`                  | -                        | GGUF  |
| *LlamaCpp*   | `llamacpp:`                   | -                        | GGUF  |
| *tabbyAPI*   | `tabbyapi:`                   | TABBYAPI_API_KEY<br>TABBYAPI_ADMIN_KEY<br>HF_API_TOKEN | EXL2, GPTQ<br>dynamic model downloads<br>dynamic model loading |

## License

MIT


## Installation

Don't. The project is still in its infancy.

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
```

```python
# with parameter overriding
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

## How to use middleware

```python
class TimingMiddleware(MiddlewareBase):

    def request(self, data):
        self.ctx.start = time.perf_counter()
        return data

    def response(self, data):
        self.ctx.duration = time.perf_counter() - self.ctx.start
        return data

ctx = SimpleNamespace() # you can also use dataclass or pydantic.BaseModel
model = aibricks.connect('openrouter:qwen/qwen-2.5-coder-32b-instruct')
model.add_middleware(TimingMiddleware(ctx))
resp = model.chat_create([{'role': 'user', 'content': 'Tell me a joke.'}])
print(f'{ctx.duration=}')
```

## How to test

```sh
# Run simple connection test for a specific provider
python3 -m aibricks.providers.lmstudio_api

# Run all tests
pytest

# Run only provider tests
pytest tests/aibricks/providers/

# Run only middleware tests
pytest tests/aibricks/middleware/
```

## Planned features

- anthropic api support
- server mode
- outlines support
- vllm support
- mamba support
- huggingfaece downloads
- more middleware
