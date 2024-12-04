import os
import aibricks

os.chdir(os.path.dirname(__file__))  # kind of ugly
cfg = aibricks.load_config("./game.yaml")

character = cfg.lookup('characters.marcus')
game_prompt = cfg.render('game_prompt', character=character)

messages = [{'role': 'system', 'content': game_prompt}]

print(character['scenario'])
print(character['first_message'])

client = aibricks.client()

while True:
    user_text = input("You: ")
    messages += [{'role': 'user', 'content': user_text}]
    response = client.chat.completions.create(model='lmstudio:', messages=messages)
    print(response)
    ai_text = response.choices[0].message.content
    print(ai_text)
    messages += [{'role': 'assistant', 'content': ai_text}]
