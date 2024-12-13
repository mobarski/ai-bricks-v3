from types import SimpleNamespace


class MiddlewareBase:

    def __init__(self):
        self.parent = None

    def request(self, data, ctx):
        return data

    def handle_response(self, response, ctx, request=None):
        return None

    def response(self, data, ctx):
        return data

    # other events can be added


class MiddlewareMixin:

    def __init__(self):
        self.middleware = []
        self.ctx = {}

    def add_middleware(self, middleware):
        self.middleware.append(middleware)
        middleware.parent = self
        middleware.ctx = self.ctx

    def run_middleware(self, event, data, **kwargs):
        for m in self.middleware:
            if hasattr(m, event):
                data = getattr(m, event)(data, m.ctx, **kwargs)
        return data
