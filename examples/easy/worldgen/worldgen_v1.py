from rich.pretty import pprint

import os
import re
import json

import aibricks
from aibricks.utils import dict_from_xml, list_from_xml

os.chdir(os.path.dirname(__file__))  # kind of ugly
cfg = aibricks.load_config('./worldgen_v1.yaml')

client = aibricks.client()

kw = cfg.lookup('parameters').copy()


def get_ai_resp_text(messages):
    resp = client.chat.completions.create(model=kw['model'], messages=messages)
    ai_text = resp.choices[0].message.content
    return ai_text


messages = [{'role': 'system', 'content': cfg.render('system_prompt', **kw)}]
messages += [{'role': 'user',  'content': cfg.render('world_prompt', **kw)}]

# world
ai_text = get_ai_resp_text(messages)
messages += [{'role': 'assistant', 'content': ai_text}]
kw['world'] = dict_from_xml(ai_text)
pprint(kw['world'])

# kingdoms
messages += [{'role': 'user', 'content': cfg.render('kingdom_prompt', **kw)}]
ai_text = get_ai_resp_text(messages)
messages += [{'role': 'assistant', 'content': ai_text}]
kw['kingdoms'] = list_from_xml(ai_text)
pprint(kw['kingdoms'])

for kingdom in kw['kingdoms']:
    # towns
    messages += [{'role': 'user', 'content': cfg.render('town_prompt', **kw, kingdom=kingdom)}]
    ai_text = get_ai_resp_text(messages)
    messages += [{'role': 'assistant', 'content': ai_text}]
    kingdom['towns'] = list_from_xml(ai_text)
    pprint(kingdom['towns'])


# save the world to a json file
world_label = re.sub(r'[^a-z0-9]', '', kw['world']['name'].lower())
with open(f'output/v1-{world_label}.json', 'w') as f:
    world_dict = {
        'world': kw['world'],
        'parameters': cfg.lookup('parameters'),
        'kingdoms': kw['kingdoms'],
    }
    json.dump(world_dict, f, indent=2)
