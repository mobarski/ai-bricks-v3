import time

from aibricks.middleware import MiddlewareBase


class TimingMiddleware(MiddlewareBase):

    def request(self, data):
        self.ctx.start = time.perf_counter()
        return data

    def response(self, data):
        self.ctx.duration = time.perf_counter() - self.ctx.start
        return data
