class Client:
    def __init__(self, connect, model=None, **kwargs):
        self.chat = Chat(self)
        self.model = model
        self.config = kwargs.pop('config', None)
        self.from_config = kwargs.pop('from_config', None)
        self._connect = connect
        self.kwargs = kwargs
        self.middleware = []

    def connect(self, model):
        return self._connect(model, config=self.config, from_config=self.from_config, **self.kwargs)

    def add_middleware(self, middleware):
        self.middleware.append(middleware)


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
        #
        common_keys = kwargs.keys() & self.client.kwargs.keys()
        kw = {}
        # client kwargs will override kwargs only if callable
        for k in kwargs:
            if k in common_keys and callable(self.client.kwargs[k]):
                kw[k] = self.client.kwargs[k](kwargs[k])
            else:
                kw[k] = kwargs[k]
        for k in self.client.kwargs:
            if k in common_keys:
                continue
            if callable(self.client.kwargs[k]):
                kw[k] = self.client.kwargs[k](None)
            else:
                kw[k] = self.client.kwargs[k]

        conn = self.client.connect(m)
        for m in self.client.middleware:
            conn.add_middleware(m)
        if kw.get('stream'):
            return conn.chat_create_stream(messages, **kw)
        else:
            return conn.chat_create(messages, **kw)
