import os
import aibricks

import rich
import re
from rich.console import Console

CHARACTER = 'anne'
MODEL = 'lmstudio:'
console = Console(width=80)


def rich_output(text):
    text = re.sub('(["][^"]*?["])', r'[yellow]\1[/]', text)
    text = re.sub('([*][^*]*?[*])', r'[cyan]\1[/]', text)
    console.print(text)


os.chdir(os.path.dirname(__file__)) # kind of ugly
cfg = aibricks.load_config("./game-v2.yaml")

character = cfg.lookup(f'characters.{CHARACTER}')
game_prompt = cfg.render('game_prompt', character=character)

messages = [{'role': 'system', 'content': game_prompt}]

rich_output(character['scenario'])
rich_output(character['first_message'])

client = aibricks.client()

ctx = {}
aux_connection = aibricks.connect('lmstudio:')
summary_middleware = aibricks.middleware.ChatSummaryMiddleware(ctx, aux_connection, max_in_context_chars=8000)
summary_middleware.debug = True
client.add_middleware(summary_middleware)

while True:
    rich_output('='*80)
    user_text = console.input("[bold white]You: ", )
    messages += [{'role': 'user', 'content': user_text}]
    response = client.chat.completions.create(model=MODEL, messages=messages)
    ai_text = response.choices[0].message.content
    rich_output('\n' + ai_text)
    messages += [{'role': 'assistant', 'content': ai_text}]
