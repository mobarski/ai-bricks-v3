import time

from aibricks.middleware import MiddlewareBase


class TimingMiddleware(MiddlewareBase):

    def request(self, data, ctx):
        ctx['timing_start'] = time.perf_counter()
        return data

    def response(self, data, ctx):
        ctx['timing_duration'] = time.perf_counter() - ctx['timing_start']
        return data
