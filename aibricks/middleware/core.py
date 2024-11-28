from types import SimpleNamespace


class MiddlewareBase:

    def __init__(self, ctx: SimpleNamespace | object):
        self.ctx = ctx
        self.parent = None

    def request(self, data):
        return data

    def response(self, data):
        return data

    # other events can be added


class MiddlewareMixin:
    middleware = []

    def add_middleware(self, middleware):
        self.middleware.append(middleware)
        middleware.parent = self

    def run_middleware(self, event, data):
        for m in self.middleware:
            if hasattr(m, event):
                data = getattr(m, event)(data)
        return data
