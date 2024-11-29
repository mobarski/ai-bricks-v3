# TESTING

- [ ] lambda x: for all kwargs (not only model)

# ACTIVE

- [ ] server (to act as provider)
- [ ] config (yaml + string.Template)

# TODO

- [ ] outlines like prompts (jinja2) ???
- [ ] streaming (REF: https://github.com/oobabooga/text-generation-webui/wiki/12-%E2%80%90-OpenAI-API#examples)
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
- [ ] two local models
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
