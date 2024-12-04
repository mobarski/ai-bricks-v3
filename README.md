## AI Bricks

Simple, unified interface to multiple Generative AI providers and local model servers.

This project is similar in scope to [AISuite](https://github.com/andrewyng/aisuite),
but with the following differences:
- stronger support for local model servers (**tabbyAPI**, **KoboldCpp**, **LMStudio**, **Ollama**, ...)
- focus on improving your application without having to change your code
- middleware for logging, usage tracking, styling, etc
- configuration driven approach
- minimal dependencies (*requests*, *pyyaml*, *jinja2*)


## Supported providers

| Provider       | Example Connection String     | Environmental Variables  | Notes |
|----------------|-------------------------------|--------------------------|-------|
| **OpenAI**     | `openai:gpt-4o-mini`          | OPENAI_API_KEY           |       |
| **Google**     | `google:gemini-1.5-flash`     | GEMINI_API_KEY           |       |
| **OpenRouter** | `openrouter:openai/gpt-4o`    | OPENROUTER_API_KEY       |       |
| **ArliAI**     | `arliai:Llama-3.1-70B-Tulu-2` | ARLIAI_API_KEY           |       |
| **XAI**        | `xai:grok-beta`               | XAI_API_KEY              |       |
| **Together**   | `together:meta-llama/Meta-Llama-3-8B-Instruct-Turbo` | TOGETHER_API_KEY |  |
| **Ollama**     | `ollama:qwen2.5-coder:7b`     | -                        | GGUF  |
| **LMStudio**   | `lmstudio:qwen2.5-14b-instruct` | -                      | GGUF<br>dynamic model loading |
| **KoboldCpp**  | `koboldcpp`                   | -                        | GGUF  |
| **LlamaCpp**   | `llamacpp`                    | -                        | GGUF  |
| **tabbyAPI**   | `tabbyapi`                    | TABBYAPI_API_KEY<br>TABBYAPI_ADMIN_KEY<br>HF_API_TOKEN | EXL2, GPTQ<br>dynamic model downloads<br>dynamic model loading |
| **dummy**      | `dummy`                       | -                        |       |

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
# parameter overriding example
client = aibricks.client(
    # any parameter can have a default value
    temperature=0.7,
    # or can be overridden by a lambda taking the original value
    model=lambda x: 'openrouter:qwen/qwen-2.5-coder-32b-instruct',
)

# somewhere else in the code
resp = client.chat.completions.create(
    model='openrouter:openai/gpt-3.5-turbo', # ignored
    messages=[{"role": "user", "content": "Tell me a joke."}],
    # default temperature=0.7 is used
)
print(resp)
```

## How to use middleware

```python
# initialize OpenAI compatible client as usual
client = aibricks.client()

# add 3 lines to create the illusion of an infinite context
ctx = {}
summary_middleware = ChatSummaryMiddleware(ctx, max_in_context_chars=12000)
client.add_middleware(summary_middleware)

# use the client as usual
resp = client.chat.completions.create(...)
```

## How to create middleware

```python
class TimingMiddleware(MiddlewareBase):

    def request(self, data, ctx):
        ctx["start"] = time.perf_counter()
        return data

    def response(self, data, ctx):
        ctx["duration"] = time.perf_counter() - ctx["start"]
        return data

ctx = {}
client = aibricks.connect('openrouter:qwen/qwen-2.5-coder-32b-instruct')
client.add_middleware(TimingMiddleware(ctx))
resp = client.chat_create([{'role': 'user', 'content': 'Tell me a joke.'}])
print(ctx)
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

## Examples

### Easy

- [game](examples/easy/game/) - simple "chat with a character", nice stepping stone for building rpg/adventure games
  - [v1](examples/easy/game/v1.py) as simple as it gets
  - [v2](#TODO) adds "infinite context" and colors
  - [v3](#TODO) ~~adds save/load/undo functionality~~
- [worldgen](examples/easy/worldgen/) - simple, hierarchical world generation (based on [this lesson](https://learn.deeplearning.ai/courses/building-an-ai-powered-game/lesson/2/hierarchical-content-generation))
  - [v1](examples/easy/worldgen/v1.py) as simple as it gets 🚧
  - [v2](#TODO) ~~adds ability to use images for the inspiration~~
- [codegen](examples/easy/codegen/) - ~~simple code generation for tiny web apps~~
  - [v1](#TODO) ~~as simple as it gets~~
  - [v2](#TODO) ~~adds UI designer role~~

## Planned features

- anthropic api support
- server mode
- outlines support
- vllm support
- mamba support
- huggingface downloads
- more middleware
