import os
import sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
import aibricks

import rich
import re

os.chdir(os.path.dirname(__file__)) # kind of ugly
cfg = aibricks.load_config("./game.yaml")

character = cfg.lookup('characters.marcus')
game_prompt = cfg.render('game_prompt', character=character)

messages = [{'role': 'system', 'content': game_prompt}]
messages += [{'role': 'assistant', 'content': character['scenario']}]
messages += [{'role': 'assistant', 'content': character['first_message']}]

print(character['scenario'])  # TODO: style text
print(character['first_message'])  # TODO: style text

client = aibricks.client()

ctx = {}
summary_middleware = aibricks.middleware.ChatSummaryMiddleware(ctx, max_in_context_chars=8000)
client.add_middleware(summary_middleware)

while True:
    user_text = input("You: ")
    messages += [{'role': 'user', 'content': user_text}]
    response = client.chat.completions.create(model='lmstudio:', messages=messages)
    ai_text = response.choices[0].message.content
    print(ai_text)  # TODO: style text
