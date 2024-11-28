from types import SimpleNamespace


class MiddlewareContext(SimpleNamespace):
    pass


class MiddlewareBase:

    # def init(self, obj, ctx, data):
    #     return data

    def data(self, obj, ctx, data):
        return data

    def raw_resp(self, obj, ctx, raw_resp):
        return raw_resp

    def resp(self, obj, ctx, resp):
        return resp

    def norm_resp(self, obj, ctx, norm_resp):
        return norm_resp


class MiddlewareMixin:
    middleware = []

    def run_middleware(self, event, ctx, data):
        for m in self.middleware:
            if hasattr(m, event):
                data = getattr(m, event)(self, ctx, data)
        return data
