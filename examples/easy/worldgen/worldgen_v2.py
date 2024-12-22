from rich.pretty import pprint

import os
import re
import json

import aibricks
from aibricks.utils import dict_from_xml, list_from_xml

os.chdir(os.path.dirname(__file__))  # kind of ugly
cfg = aibricks.load_config('./worldgen_v2.yaml')

client = aibricks.client()

kw = cfg.lookup('parameters').copy()


def get_ai_resp_text(messages):
    resp = client.chat.completions.create(model=kw['model'], messages=messages)
    ai_text = resp.choices[0].message.content
    return ai_text


def prompt_and_parse(prompt_name, parse_fn, **extra_kwargs):
    prompt_kwargs = {**kw, **extra_kwargs}
    messages.append({'role': 'user', 'content': cfg.render(prompt_name, **prompt_kwargs)})
    ai_text = get_ai_resp_text(messages)
    messages.append({'role': 'assistant', 'content': ai_text})
    result = parse_fn(ai_text)
    pprint(result)
    return result


# Initial world and kingdom generation
messages = [{'role': 'system', 'content': cfg.render('system_prompt', **kw)}]
kw['world'] = prompt_and_parse('world_prompt', dict_from_xml)
kw['kingdoms'] = prompt_and_parse('kingdom_prompt', list_from_xml)

# Generate details for each kingdom
for kingdom in kw['kingdoms']:
    kingdom['towns'] = prompt_and_parse('town_prompt', list_from_xml, kingdom=kingdom)

    for town in kingdom['towns']:
        town['npcs'] = prompt_and_parse('npc_prompt', list_from_xml, town=town)
        town['locations'] = prompt_and_parse('location_prompt', list_from_xml, town=town)
        town['events'] = prompt_and_parse('event_prompt', list_from_xml, town=town)

# save the world to a json file
world_label = re.sub(r'[^a-z0-9]', '', kw['world']['name'].lower())
with open(f'output/v2-{world_label}.json', 'w') as f:
    world_dict = {
        'world': kw['world'],
        'parameters': cfg.lookup('parameters'),
        'kingdoms': kw['kingdoms'],
    }
    json.dump(world_dict, f, indent=2)
