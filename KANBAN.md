# TESTING

- [ ] chat summary middleware
- [ ] test middleware with client.chat.completions.create

# ACTIVE

- [ ] config (yaml + jinja2)

# PAUSED

- [ ] server (to act as provider)

# TODO

- [ ] streaming (REF: https://github.com/oobabooga/text-generation-webui/wiki/12-%E2%80%90-OpenAI-API#examples)

- [ ] add config to middleware call args
- [ ] two local models
- [ ] outlines like prompts (jinja2) ???
- [ ] parallelism

- [ ] structured output (openai)
- [ ] outlines server provider
- [ ] structured output (others)
- [ ] structured output (outlines)

- [ ] terminal UI

- [ ] roles
- [ ] characters

- [ ] xml
- [ ] vfs
- [ ] tools
- [ ] xml tools
- [ ] diff tools

- [ ] vision
- [ ] memory

# TODO (providers)

- [ ] base url change
- [ ] anthropics API
- [ ] vllm server
- [ ] mamba models server
- [ ] oobabooga server

# TODO (middleware)

- [ ] exception handling in the middleware
- [ ] error handling in the middleware
- [ ] retries in the middleware
- [ ] cacheing middleware
- [ ] usage middleware
- [ ] prices middleware + config
- [ ] output formating middleware (rich)
- [ ] judge LLMs in the middleware

# DONE

- [x] change context type to dict
- [x] add context to middleware call args (to make code prettier)
- [x] lambda x: for all kwargs (not only model)
- [x] logging middleware (sqlite)
- [x] README: middleware
- [x] timing
- [x] middleware
- [x] config as separate part (in pyproject.toml)
- [x] fix: arliai test
- [x] client(model=lambda x:...)
- [x] unit tests structure (providers)
- [x] drop-in OpenaAI API replacement

# OUT OF SCOPE

- completions endpoint
