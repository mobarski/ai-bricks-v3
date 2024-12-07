from types import SimpleNamespace


class MiddlewareBase:

    def __init__(self, ctx: dict):
        self.ctx = ctx
        self.parent = None

    def request(self, data, ctx):
        return data

    def handle_response(self, response, ctx, request=None):
        return None

    def response(self, data, ctx):
        return data

    # other events can be added


class MiddlewareMixin:
    middleware = []

    def add_middleware(self, middleware):
        self.middleware.append(middleware)
        middleware.parent = self

    def run_middleware(self, event, data, **kwargs):
        for m in self.middleware:
            if hasattr(m, event):
                data = getattr(m, event)(data, m.ctx, **kwargs)
        return data
