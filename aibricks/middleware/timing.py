import time

from aibricks.middleware import MiddlewareBase


class TimingMiddleware(MiddlewareBase):

    def data(self, obj, ctx, data):
        ctx.start = time.perf_counter()
        return data

    def resp(self, obj, ctx, resp):
        ctx.duration = time.perf_counter() - ctx.start
        return resp
