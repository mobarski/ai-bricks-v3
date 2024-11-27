class Client:
    def __init__(self, connect, model=None, **kwargs):
        self.chat = Chat(self)
        self.connect = connect
        self.model = model
        self.kwargs = kwargs


class Chat:
    def __init__(self, client):
        self.client = client
        self.completions = ChatCompletions(client)


class ChatCompletions:
    def __init__(self, client):
        self.client = client

    def create(self, model, messages, **kwargs):
        if callable(self.client.model):
            m = self.client.model(model)
        elif self.client.model:
            m = self.client.model
        else:
            m = model
        connect = self.client.connect
        return connect(m, **self.client.kwargs).chat_create(messages=messages, **kwargs)
