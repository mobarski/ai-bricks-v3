from types import SimpleNamespace

from aibricks.middleware import MiddlewareBase


class ChatSummaryMiddleware(MiddlewareBase):

    def __init__(self, ctx: SimpleNamespace | object, llm_client, max_in_context_chars=2000):
        super().__init__(ctx)
        self.llm_client = llm_client
        self.first_msg_idx = 0
        self.max_in_context_chars = max_in_context_chars
        self.current_summary = ''
        # TODO: skip system messages

    def request(self, data):
        messages = data['data']['messages']
        data['data']['messages'] = self.insert_summary(messages)
        self.ctx.summary = self.current_summary # XXX
        return data

    def insert_summary(self, messages):
        current_context_len = len(str(messages[self.first_msg_idx:]))
        if current_context_len < self.max_in_context_chars:
            return messages
        current_cnt = len(messages) - self.first_msg_idx
        leftover_cnt = min(1, current_cnt // 3)
        delta_cnt = current_cnt - leftover_cnt
        delta_messages = messages[self.first_msg_idx : -leftover_cnt]
        self.first_msg_idx += delta_cnt
        summary = self.create_summary(self.current_summary, delta_messages)
        self.current_summary = summary
        summary_message = self.get_summary_message(summary)
        new_messages = [summary_message] + messages[-leftover_cnt:]
        return new_messages

    def create_summary(self, current_summary, delta_messages):
        # TODO: better prompt
        system_prompt = "You are a chat summarizer. " \
            "Create a summary of the chat history below. " \
            "Summarize events, entities, and topics. " \
            "The maximum length of the summary is a quarter of the chat history " \
            "but try to keep it short. " \
            "Only include the summary in the response. "
        messages = [{"role": "system", "content": system_prompt}]
        if current_summary:
            messages += [self.get_summary_message(current_summary)]
        messages += [self.get_messages_message(delta_messages)]
        print(f'\n\ncreate_summary: {messages=}')
        resp = self.llm_client.chat_create(messages=messages)
        new_summary = resp['choices'][0]['message']['content']
        return new_summary

    def get_summary_message(self, summary):
        return {
            "role": "user",
            "content": f'SUMMARY OF PREVIOUS CHAT:\n\n{summary}'
        }

    def get_messages_message(self, messages):
        history = ''
        for msg in messages:
            history += f'{msg["role"]}: {msg["content"]}\n'
        return {
            "role": "user",
            "content": f'CHAT HISTORY:\n\n{history}'
        }
