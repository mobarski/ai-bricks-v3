class Client:
    def __init__(self, connect):
        self.chat = Chat(self)
        self.connect = connect


class Chat:
    def __init__(self, client):
        self.client = client
        self.completions = ChatCompletions(client)


class ChatCompletions:
    def __init__(self, client):
        self.client = client

    def create(self, model, messages, **kwargs):
        connect = self.client.connect
        return connect(model).chat_create(messages=messages, **kwargs)
