import os
import aibricks

import rich
import re
from rich.console import Console
console = Console()


def rich_output(text):
    text = re.sub('(["][^"]*?["])', r'[blue]\1[/]', text)
    text = re.sub('([*][^*]*?[*])', r'[yellow]\1[/]', text)
    rich.print(text)


os.chdir(os.path.dirname(__file__)) # kind of ugly
cfg = aibricks.load_config("./game.yaml")

character = cfg.lookup('characters.anne')
game_prompt = cfg.render('game_prompt', character=character)

messages = [{'role': 'system', 'content': game_prompt}]

rich_output(character['scenario'])
rich_output(character['first_message'])

client = aibricks.client()

ctx = {}
summary_middleware = aibricks.middleware.ChatSummaryMiddleware(ctx, max_in_context_chars=8000)
client.add_middleware(summary_middleware)

while True:
    user_text = console.input("[bold white]You: ", )
    messages += [{'role': 'user', 'content': user_text}]
    response = client.chat.completions.create(model='lmstudio:', messages=messages)
    ai_text = response.choices[0].message.content
    rich_output('\n' + ai_text)
    messages += [{'role': 'assistant', 'content': ai_text}]
