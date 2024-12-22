import os
import aibricks

import re
from rich.console import Console


def rich_output(text):
    text = re.sub('(["][^"]*?["])', r'[yellow]\1[/]', text)
    text = re.sub('([*][^*]*?[*])', r'[cyan]\1[/]', text)
    console.print(text)


# SETUP
os.chdir(os.path.dirname(__file__))
cfg = aibricks.load_config("./game_v3.yaml")

client = aibricks.client(from_config='models.default', config=cfg)
WIDTH = cfg.lookup('game.console-width')
console = Console(width=WIDTH)

# GAME PROMPT
character_id = cfg.lookup('game.character')
character = cfg.lookup('characters.' + character_id)
game_prompt = cfg.render('game_prompt', character=character)

messages = [{'role': 'system', 'content': game_prompt}]

# GAME LOOP
rich_output(character['scenario'])
rich_output(character['first_message'])
while True:
    rich_output('='*WIDTH)
    user_text = console.input("[bold white]You: ", )
    messages += [{'role': 'user', 'content': user_text}]
    response = client.chat.completions.create(None, messages=messages)
    ai_text = response.choices[0].message.content
    rich_output('\n' + ai_text)
    messages += [{'role': 'assistant', 'content': ai_text}]
