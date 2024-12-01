import time

from aibricks.middleware import MiddlewareBase


class TimingMiddleware(MiddlewareBase):

    def request(self, data, ctx):
        ctx['start'] = time.perf_counter()
        return data

    def response(self, data, ctx):
        ctx['duration'] = time.perf_counter() - ctx['start']
        return data
