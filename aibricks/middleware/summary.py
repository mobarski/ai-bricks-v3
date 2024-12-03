from aibricks.middleware import MiddlewareBase


class ChatSummaryMiddleware(MiddlewareBase):
    # Class constants
    DEFAULT_MAX_CONTEXT_CHARS = 2000
    MIN_MESSAGES_TO_KEEP = 1
    SUMMARY_LENGTH_RATIO = 0.25

    def __init__(self,
                 ctx: dict,
                 connection=None,
                 max_in_context_chars=DEFAULT_MAX_CONTEXT_CHARS):
        super().__init__(ctx)
        self.connection = connection
        self.first_msg_idx = 0
        self.max_in_context_chars = max_in_context_chars
        if 'summary' not in ctx:
            ctx['summary'] = ''
        self.current_summary = ctx['summary']
        self.debug = False

    # Main request handling
    # ---------------------
    def request(self, data, ctx):
        messages = data['data']['messages']
        data['data']['messages'] = self.insert_summary(messages)
        ctx['summary'] = self.current_summary
        return data

    def insert_summary(self, messages: list[dict]) -> list[dict]:
        total_history_length = len(str(messages[self.first_msg_idx:]))
        if total_history_length < self.max_in_context_chars:
            return messages

        message_count = len(messages) - self.first_msg_idx
        messages_to_keep = max(self.MIN_MESSAGES_TO_KEEP, message_count // 3)
        messages_to_summarize = message_count - messages_to_keep

        history_to_summarize = messages[self.first_msg_idx: -messages_to_keep]
        self.first_msg_idx += messages_to_summarize

        updated_summary = self.create_summary(self.current_summary, history_to_summarize)
        self.current_summary = updated_summary
        summary_msg = self.get_summary_message(updated_summary)

        return [summary_msg] + messages[-messages_to_keep:]

    # Summary generation
    # ------------------
    def create_summary(self, current_summary: str, new_messages: list[dict]) -> str:
        system_prompt = (
            "You are chat summarizer.\n"
            "Your task is to:\n"
            "1. Create a summary of the provided chat history\n"
            "2. Include key events, entities, and topics\n"
            "3. Keep summary length under 25% of chat history\n"
            "4. Be as concise as possible\n"
            "Provide only the summary in your response."
        )

        summary_request = [{"role": "system", "content": system_prompt}]

        if current_summary:
            summary_request.append(self.get_summary_message(current_summary))

        summary_request.append(self.get_messages_message(new_messages))

        if self.debug:
            print(f'\n\ncreate_summary request: {summary_request=}')

        conn = self.connection or self.parent
        response = conn.chat_create(messages=summary_request)
        return response['choices'][0]['message']['content']

    # Message formatting
    # ------------------
    def get_summary_message(self, summary: str) -> dict:
        return {
            "role": "user",
            "content": f'SUMMARY OF PREVIOUS CHAT:\n\n{summary}'
        }

    def get_messages_message(self, messages: list[dict]) -> dict:
        chat_history = '\n'.join(
            f'{msg["role"]}: {msg["content"]}'
            for msg in messages
        )
        return {
            "role": "user",
            "content": f'CHAT HISTORY:\n\n{chat_history}'
        }
